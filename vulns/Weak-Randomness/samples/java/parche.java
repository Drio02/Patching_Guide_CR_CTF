import java.security.SecureRandom;
import java.util.HexFormat;

public class Tokens {
    // Patch: SecureRandom (thread-safe, no hace falta sembrarlo)
    private static final SecureRandom RNG = new SecureRandom();

    public static String sessionToken() {
        byte[] b = new byte[16];
        RNG.nextBytes(b);
        return HexFormat.of().formatHex(b);
    }

    public static int resetCode() {
        return RNG.nextInt(900000) + 100000;
    }
}
