using System.Xml;
using Microsoft.AspNetCore.Mvc;

[ApiController]
public class ImportController : ControllerBase
{
    // Vuln: DtdProcessing.Parse + XmlUrlResolver resuelven entidades externas
    [HttpPost("/import")]
    public string Import([FromBody] string xml)
    {
        var settings = new XmlReaderSettings
        {
            DtdProcessing = DtdProcessing.Parse,
            XmlResolver = new XmlUrlResolver(),
        };
        using var reader = XmlReader.Create(new StringReader(xml), settings);
        var doc = new XmlDocument();
        doc.Load(reader);
        return doc.SelectSingleNode("//body")?.InnerText ?? "";
    }
}
