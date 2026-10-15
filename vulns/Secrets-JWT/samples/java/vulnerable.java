import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import javax.crypto.SecretKey;

public class TokenService {
    // Vuln 1: clave hardcodeada en el codigo
    private static final SecretKey KEY =
        Keys.hmacShaKeyFor("this-is-the-jwt-secret-key-32-bytes!".getBytes(StandardCharsets.UTF_8));

    // Vuln 2: parsea tokens SIN firma (alg: none)
    public String user(String token) {
        return Jwts.parser().unsecured().build()
                   .parseUnsecuredClaims(token).getPayload().getSubject();
    }
}
