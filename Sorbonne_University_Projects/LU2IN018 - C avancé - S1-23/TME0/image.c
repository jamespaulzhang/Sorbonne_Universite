#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "image.h"

 #define TMP_STR_SIZE 256

image_t *creer_image()
{
  /* a completer */
  image_t *image = (image_t *)malloc(sizeof(image_t));
  if (image == NULL)
  {
    fprintf(stderr, "Erreur lors de l'allocation de mémoire pour l'image.\n");
    exit(1);
  }
  image->w = 0;
  image->h = 0;
  image->buff = NULL;
  return image;
}

void detruire_image(image_t *p)
{
  /* a completer */
  if (p != NULL)
  {
    free(p->buff);
    free(p);
  }  
}

void negatif(image_t *img)
{ 
  /* a completer */
  /* img->buff[0] permet d'acceder au premier pixel de l'image */
  if (img != NULL && img->buff != NULL)
  {
    int pix = img->h * img->w;
    for (int i = 0; i < pix; i++)
    {
      img->buff[i] = 255 - img->buff[i];
    }
  }
}

void modifier_lumin(image_t *img, float pourcent)
{
  /* a completer */
  if (img != NULL && img->buff != NULL)
  {
    int pix = img->h * img->w;
    for (int i = 0; i < pix; i++)
    {
      int nouvelle_valeur = (int)(img->buff[i] * pourcent);
      img->buff[i] = (nouvelle_valeur > 255) ? 255 : (unsigned char)nouvelle_valeur;
    }
  } 
}


image_t *rotation(image_t *src, int angle)
{
  if (src == NULL || src->buff == NULL)
  {
    fprintf(stderr, "Image source invalide pour la rotation.\n");
    return NULL;
  }

  if (angle % 90 != 0)
  {
    fprintf(stderr, "Angle de rotation invalide. Utilisez des multiples de 90.\n");
    return NULL;
  }

  int nb_rotations = (angle / 90) % 4;

  image_t *dst = creer_image();
  dst->w = src->w;
  dst->h = src->h;
  dst->buff = (unsigned char *)malloc(src->w * src->h * sizeof(unsigned char));

  for (unsigned long i = 0; i < src->h; i++)
  {
    for (unsigned long j = 0; j < src->w; j++)
    {
      unsigned long new_i, new_j;
      switch (nb_rotations)
      {
      case 1:
        new_i = j;
        new_j = src->h - 1 - i;
        break;
      case 2:
        new_i = src->h - 1 - i;
        new_j = src->w - 1 - j;
        break;
      case 3:
        new_i = src->w - 1 - j;
        new_j = i;
        break;
      default: // Pas de rotation
        new_i = i;
        new_j = j;
        break;
      }
      VAL(dst, new_i, new_j) = VAL(src, i, j);
    }
  }

  return dst;
}


image_t *charger_image_pgm(char *nom_fichier)
{
  FILE *f;
  image_t *img;
  unsigned int nb_ng;
  char tmp_str[TMP_STR_SIZE];
  enum format {BIN, ASCII} pgm_form;

  /* Ouverture du fichier en lecture */
  f=fopen(nom_fichier, "r");


  if (!f)
    {
      /* on ecrit sur le flux d'erreur */
      fprintf(stderr, "impossible d'ouvrir le fichier %s\n", nom_fichier);
      return NULL;
    }

  /* on lit une ligne en supprimant les eventuels commentaires */
  do
    fgets(tmp_str, TMP_STR_SIZE, f);
  while (*tmp_str == '#');

  /* on determine le format */
  if ( !strcmp(tmp_str, "P5\n"))
    pgm_form = BIN;
  else if ( !strcmp(tmp_str, "P2\n"))
    pgm_form = ASCII;
  else
    {
      fprintf(stderr, "format fichier non pgm\n");
      return NULL;
    }

  img = creer_image();

  /* on lit une ligne en supprimant les eventuels commentaires */
  do
    fgets(tmp_str, TMP_STR_SIZE, f);
  while (*tmp_str == '#');

  /* on determine la largeur et la hauteur de l'image */
  if (sscanf(tmp_str, "%ld %ld\n", &(img->w), &(img->h)) != 2)
    {
      /* si le sscanf n'a pas lu les deux entiers longs attendus: */
      fprintf(stderr, "format fichier non pgm\n");
      detruire_image(img);
      return NULL;
    }

  /* on lit une ligne en supprimant les eventuels commentaires */
  do
    fgets(tmp_str, TMP_STR_SIZE, f);
  while (*tmp_str == '#');

  /* on lit le niveau de gris */
  if (sscanf(tmp_str, " %d ", &nb_ng) != 1)
    {
      /* si le sscanf n'a pas lu l'entier attendu: */
      fprintf(stderr, "format fichier non pgm\n");
      detruire_image(img);
      return NULL;
    }

  if (nb_ng != 255)
    {
      fprintf(stderr, "Nombre de ng different de 255: erreur\n");
      detruire_image(img);
      return NULL;
    }

  /* on alloue l'espace pour stocker l'image */
  img->buff = (unsigned char *) malloc(img->w * img->h * sizeof (unsigned char));

  /* on lit l'image en prenant en compte le format */
  if ( pgm_form == BIN )
    {
      if (fread(img->buff, img->w, img->h, f) != img->h)
        {
          fprintf(stderr, "fichier image imcomplet!\n");
          return NULL;
        }
    }
  else
    {
      unsigned int i,j;
      unsigned char *p = img->buff;
      for ( i = 0; i < img->h; i++)
        for ( j = 0; j < img->w; j++)
          fscanf(f, "%hhu ", p++);
    }

  fclose(f);
  return img;
}

int sauver_image_pgm(char *nom_fichier, image_t *img)
{
  FILE *f;

  f=fopen(nom_fichier, "w");

  if (!f)
    {
      fprintf(stderr, "impossible d'ouvrir le fichier %s\n", nom_fichier);
      return 0;
    }

  fprintf(f, "P5\n");
  fprintf(f, "#Genere par guimp UPMC.\n");
  fprintf(f, "%ld %ld\n", img->w, img->h);
  fprintf(f, "255\n");

  fwrite(img->buff, img->w, img->h, f);
  fclose(f);
  return 1;
}


int main(void) {
  /* a completer */
  image_t *image = creer_image();
  if (image == NULL)
  {
    fprintf(stderr, "Erreur lors de la création de l'image.\n");
    return 1;
  }
  negatif(image);
  detruire_image(image);
  return 0;
}
