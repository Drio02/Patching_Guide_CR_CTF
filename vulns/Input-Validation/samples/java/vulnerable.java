import java.util.regex.Pattern;
import org.springframework.web.bind.annotation.*;

@RestController
public class ShopController {

    // Vuln 1: el request se bindea directo a la entidad JPA -> mass assignment
    @PostMapping("/register")
    public User register(@RequestBody User user) {     // {"username":"x","password":"y","admin":true}
        return userRepo.save(user);
    }

    // Vuln 2: cantidad negativa y overflow en la multiplicacion
    @PostMapping("/buy")
    public String buy(@RequestParam int qty, @RequestParam String item, @SessionAttribute String user) {
        int total = qty * PRICES.get(item);             // qty = -1 o qty = 1_000_000_000 (overflow)
        Account acc = accountRepo.findByOwner(user);
        if (acc.getCredits() < total) return "not enough credits";
        acc.setCredits(acc.getCredits() - total);
        accountRepo.save(acc);
        return "flag".equals(item) ? FLAG : "ok";
    }

    // Vuln 3: find() busca una subcadena, no valida el string completo
    private static final Pattern ID = Pattern.compile("[a-f0-9]{16}");
    @GetMapping("/note")
    public Note note(@RequestParam String id) {
        if (!ID.matcher(id).find()) throw new IllegalArgumentException();   // "../../x0123456789abcdef" pasa
        return noteRepo.findByPublicId(id);
    }
}
