#include "fat.h"
#include <string.h>
#include <stdio.h>

int file_found (char * file ) {
  int i;
  struct ent_dir * pt = pt_DIR;

  for (i=0; i< NB_DIR; i++) {
    if ((pt->del_flag) && (!strcmp (pt->name, file))) 
      return 0;
    pt++;
  }
  /* finchier n'existe pas */
  return 1;
}


void list_fat () {
  int i;
  short *pt = pt_FAT;
  for (i=0; i < NB_ENT_FAT; i++) {
    if (*pt)
      printf ("%d ",i);
    pt++;
  }
  printf ("\n");
}


void list_dir() {
  int i;
  struct ent_dir *pt = pt_DIR;
  int total_files = 0;

  for (i = 0; i < NB_DIR; i++) {
    if (pt->del_flag) {  // Si entrée occupée
      printf("Nom du fichier: %s, Taille: %d\n", pt->name, pt->size);
      printf("Blocs: ");
      int bloc = pt->first_bloc;

      while (bloc != FIN_FICHIER) {
        printf("%d ", bloc);
        bloc = pt_FAT[bloc];
      }

      printf("\n");
      total_files++;
    }
    pt++;
  }

  printf("Total de fichiers: %d\n", total_files);
}


int cat_file(char *file) {
  struct ent_dir *pt = pt_DIR;
  int i;

  for (i = 0; i < NB_DIR; i++) {
    if (pt->del_flag && strcmp(pt->name, file) == 0) {

      if (pt->size == 0 || pt->first_bloc == FIN_FICHIER) {
        printf("(fichier vide)\n");
        return 0;
      }

      char buffer[SIZE_SECTOR];
      short bloc = pt->first_bloc;

      while (bloc != FIN_FICHIER && bloc >= 0 && bloc < NB_ENT_FAT) {
        if (read_sector(bloc, buffer) == -1) {
          printf("Erreur de lecture du bloc %d\n", bloc);
          return -1;
        }
        fwrite(buffer, 1, SIZE_SECTOR, stdout);
        bloc = pt_FAT[bloc];
      }

      printf("\n");
      return 0;
    }
    pt++;
  }

  printf("Fichier '%s' non trouvé\n", file);
  return -1;
}


int mv_file(char *file1, char *file2) {
  if (file_found(file1)) {
    return -1;
  }
  
  if (file_found(file2) == 0) {
    return -1;
  }

  struct ent_dir *pt = pt_DIR;
  for (int i = 0; i < NB_DIR; i++) {
    if ((pt[i].del_flag) && (strcmp(pt[i].name, file1) == 0)) {
      strncpy(pt[i].name, file2, 8);
      pt[i].name[8] = '\0';

      if (write_DIR_FAT_sectors() == -1) {
        return -1;
      }
      return 0;
    }
  }
  return -1; // ne devrait jamais arriver
}


int delete_file(char *file) {
  struct ent_dir *pt = pt_DIR;
  int i;

  for (i = 0; i < NB_DIR; i++) {
    if (pt->del_flag && strcmp(pt->name, file) == 0) {
      
      short bloc = pt->first_bloc;
      short next;

      while (bloc != FIN_FICHIER) {
        next = pt_FAT[bloc];
        pt_FAT[bloc] = 0; // On marque le bloc comme libre
        bloc = next;
      }
      pt->del_flag = 0; // Marquer l'entrée également comme libre

      if (write_DIR_FAT_sectors() == -1) {
        printf("Erreur d'écriture sur le disque\n");
        return -1;
      }
      return 0;
    }
    pt++;
  }
  printf("Fichier '%s' non trouvé\n", file);

  return -1;
}


int create_file(char *file) {
  if (file_found(file) == 0) {
    printf("Erreur : le fichier '%s' existe déjà.\n", file);
    return -1;
  }

  struct ent_dir *pt = pt_DIR;
  for (int i = 0; i < NB_DIR; i++) {
    if (pt->del_flag == 0) {  // entrée libre
      pt->del_flag = 1;
      strncpy(pt->name, file, 8);
      pt->name[8] = '\0';
      pt->first_bloc = FIN_FICHIER;
      pt->last_bloc = FIN_FICHIER;
      pt->size = 0;

      if (write_DIR_FAT_sectors() == -1) {
        printf("Erreur d'écriture sur disque.\n");
        return -1;
      }

      return 0;
    }
    pt++;
  }
  printf("Erreur : répertoire plein, impossible de créer le fichier '%s'.\n", file);
  return -1;
}


short alloc_bloc() {
  for (int i = 0; i < NB_ENT_FAT; i++) {
    if (pt_FAT[i] == 0) {  // Bloc libre
      pt_FAT[i] = FIN_FICHIER;
      return i;
    }
  }
  return -1;
}

 	
int append_file(char* file, char* buffer, short size) {
  if (file_found(file)) {
    return -1;
  }

  struct ent_dir* pt = pt_DIR;
  int i;
  for (i = 0; i < NB_DIR; i++) {
    if (pt->del_flag && strcmp(pt->name, file) == 0) {
      break;
    }
    pt++;
  }

  short blocs_necessaires = size / SIZE_SECTOR;
  short reste = size % SIZE_SECTOR;  // Reste qui ne remplira pas un bloc entier
  short bloc;

  for (int j = 0; j < blocs_necessaires; j++) {
    bloc = alloc_bloc();
    if (bloc == -1) {
      return -1;  // Plus de blocs disponibles
    }

    if (write_sector(bloc, buffer + j * SIZE_SECTOR) == -1) {
      return -1;
    }

    if (pt->first_bloc == -1) {
      pt->first_bloc = bloc;
      pt->last_bloc = bloc;
    } else {
      pt_FAT[pt->last_bloc] = bloc;
      pt->last_bloc = bloc;
    }

    pt_FAT[bloc] = FIN_FICHIER;
  }

  if (reste > 0) {
    bloc = alloc_bloc();
    if (bloc == -1) {
      return -1;
    }

    if (write_sector(bloc, buffer + blocs_necessaires * SIZE_SECTOR) == -1) {
      return -1;
    }

    pt_FAT[pt->last_bloc] = bloc;
    pt->last_bloc = bloc;
    pt_FAT[bloc] = FIN_FICHIER;
  }
  
  pt->size += size;

  if (write_DIR_FAT_sectors() == -1) {
    return -1;
  }
  return 0;
}


struct ent_dir*  read_dir (struct ent_dir *pt_ent ) {
  /* A COMPLETER */  
}
