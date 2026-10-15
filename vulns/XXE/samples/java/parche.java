import java.io.ByteArrayInputStream;
import javax.xml.XMLConstants;
import javax.xml.parsers.*;
import org.w3c.dom.Document;
import org.springframework.web.bind.annotation.*;

@RestController
public class ImportController {

    private static DocumentBuilderFactory safeFactory() throws ParserConfigurationException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        // Patch: prohibir DOCTYPE por completo (bloquea XXE y billion laughs)
        dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        // Refuerzos por si el DOCTYPE tuviera que permitirse:
        dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
        dbf.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        dbf.setAttribute(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
        dbf.setXIncludeAware(false);
        dbf.setExpandEntityReferences(false);
        return dbf;
    }

    @PostMapping(value = "/import", consumes = "application/xml")
    public String importNote(@RequestBody byte[] xml) throws Exception {
        Document doc = safeFactory().newDocumentBuilder().parse(new ByteArrayInputStream(xml));
        return doc.getElementsByTagName("body").item(0).getTextContent();
    }
}
