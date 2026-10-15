import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import java.nio.file.*;
import java.security.SecureRandom;
import java.util.HexFormat;
import javax.crypto.SecretKey;

public class TokenService {
    private final SecretKey key;

    // Patch 1: clave aleatoria persistida en un volumen (o en la variable JWT_SECRET)
    public TokenService() throws Exception {
        String hex = System.getenv("JWT_SECRET");
        if (hex == null) {
            Path p = Paths.get("/data/jwt_secret");
            if (!Files.exists(p)) {
                byte[] b = new byte[32];
                new SecureRandom().nextBytes(b);
                Files.writeString(p, HexFormat.of().formatHex(b));
            }
            hex = Files.readString(p).trim();
        }
        key = Keys.hmacShaKeyFor(HexFormat.of().parseHex(hex));
    }

    // Patch 2: verifyWith exige firma valida con esta clave; rechaza alg: none
    public String user(String token) {
        return Jwts.parser().verifyWith(key).build()
                   .parseSignedClaims(token).getPayload().getSubject();
    }
}
