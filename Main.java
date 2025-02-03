public class Main {
    public static void main(String[] args) {

        int Val = 5;
        // System.out.print(square(Val));
        System.out.print(losange(Val));

    }

    private static String square(int Val) {

        String stars = "";

        for (int i = 0; i < Val; i++) {

            for (int j = 0; j < Val; j++) {
                stars += "*";
            }
            stars += "\n";
        }

        return stars;

    }

    private static String losange(int Val) {
        String losange = "";

        String blank = " ";

        for (int i = 0; i < Val * 2; i++) {
            if (i < Val) {
                for (int k = i; k < Val; k++) {
                    losange += blank;
                }
                for (int k = 0; k <= i; k++) {
                    losange += "**";
                }
            } else {
                for (int k = i; k >= Val; k--) {
                    losange += blank;
                }
                for (int k = i; k < Val * 2; k++) {
                    losange += "**";
                }
            }
            losange += "\n";
        }
        return losange;
    }

}

public class Main {
    public static void main(String[] args) {
        int Val = 5;
        line(Val, 0);
        sLine(Val, 0);
    }

    private static void line(int valMax, int i) {
        if (i >= valMax) {
            return;
        }
        blank(valMax - i, 0);
        stars(valMax, valMax - i);
        System.out.println("");
        line(valMax, i + 1);
    }

    private static void sLine(int valMax, int i) {
        if (i >= valMax) {
            return;
        }
        sBlank(valMax, valMax - i);
        sStars(valMax - i, 0);
        System.out.println("");
        sLine(valMax, i + 1);
    }

    private static void sBlank(int valMax, int i) {
        if (i > valMax) {
            return;
        }
        System.out.print(" ");
        sBlank(valMax, i + 1);
    }

    private static void sStars(int valMax, int i) {
        if (i >= valMax) {
            return;
        }
        System.out.print("**");
        sStars(valMax, i + 1);
    }

    private static void blank(int valMax, int i) {
        if (i >= valMax) {
            return;
        }
        System.out.print(" ");
        blank(valMax, i + 1);
    }

    private static void stars(int valMax, int i) {
        if (i > valMax) {
            return;
        }
        System.out.print("**");
        stars(valMax, i + 1);
    }
}
