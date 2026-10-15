using System.Runtime.Serialization.Formatters.Binary;
using Newtonsoft.Json;
using Microsoft.AspNetCore.Mvc;

[ApiController]
public class PrefsController : ControllerBase
{
    // Vuln 1: BinaryFormatter (obsoleto e inseguro por diseno)
    [HttpPost("/prefs/binary")]
    public string LoadBinary([FromBody] string b64)
    {
        var bf = new BinaryFormatter();
        using var ms = new MemoryStream(Convert.FromBase64String(b64));
        var p = (Prefs)bf.Deserialize(ms);      // gadgets de ysoserial.net -> RCE
        return p.Theme;
    }

    // Vuln 2: Json.NET con TypeNameHandling.All acepta "$type" del cliente
    [HttpPost("/prefs/json")]
    public string LoadJson([FromBody] string json)
    {
        var settings = new JsonSerializerSettings { TypeNameHandling = TypeNameHandling.All };
        var p = JsonConvert.DeserializeObject<Prefs>(json, settings);
        return p.Theme;
    }
}

[Serializable]
public class Prefs { public string Theme { get; set; } }
