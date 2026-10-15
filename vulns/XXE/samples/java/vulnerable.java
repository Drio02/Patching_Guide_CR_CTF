import java.io.ByteArrayInputStream;
import javax.xml.parsers.*;
import org.w3c.dom.Document;
import org.springframework.web.bind.annotation.*;

@RestController
public class ImportController {

    // Vuln: DocumentBuilderFactory resuelve entidades externas por defecto
    @PostMapping(value = "/import", consumes = "application/xml")
    public String importNote(@RequestBody byte[] xml) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        Document doc = dbf.newDocumentBuilder().parse(new ByteArrayInputStream(xml));
        return doc.getElementsByTagName("body").item(0).getTextContent();
    }
}
