using System.Xml;
using Microsoft.AspNetCore.Mvc;

[ApiController]
public class ImportController : ControllerBase
{
    // Patch: prohibir DTD y sin resolver
    [HttpPost("/import")]
    public ActionResult<string> Import([FromBody] string xml)
    {
        var settings = new XmlReaderSettings
        {
            DtdProcessing = DtdProcessing.Prohibit,
            XmlResolver = null,
        };
        try
        {
            using var reader = XmlReader.Create(new StringReader(xml), settings);
            var doc = new XmlDocument { XmlResolver = null };
            doc.Load(reader);
            return doc.SelectSingleNode("//body")?.InnerText ?? "";
        }
        catch (XmlException)
        {
            return BadRequest();
        }
    }
}
