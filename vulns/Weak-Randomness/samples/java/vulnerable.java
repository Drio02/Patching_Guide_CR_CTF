import java.util.Random;

public class Tokens {
    // Vuln: java.util.Random es un LCG de 48 bits; dos salidas revelan el estado
    private static final Random RNG = new Random();

    public static String sessionToken() {
        return Long.toHexString(RNG.nextLong()) + Long.toHexString(RNG.nextLong());
    }

    // Vuln: semilla con la hora
    public static int resetCode() {
        return new Random(System.currentTimeMillis()).nextInt(900000) + 100000;
    }
}
