public class TestFigure {
    public static void main(String[] args) {
        Figure[] figures = new Figure[4];
        figures[0] = new Rectangle(4, 5);
        figures[1] = new Carre(3);
        figures[2] = new Ellipse(2, 3);
        figures[3] = new Cercle(4);

        for (Figure figure : figures) {
            System.out.println("Surface : " + figure.surface());
            if (figure instanceof Figure2D) {
                System.out.println("Périmètre : " + ((Figure2D) figure).perimetre());
            }
            System.out.println();
        }
    }
}