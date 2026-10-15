using System.Text.Json;
using Microsoft.AspNetCore.Mvc;

[ApiController]
public class PrefsController : ControllerBase
{
    // Patch: System.Text.Json no resuelve tipos desde el payload
    [HttpPost("/prefs/json")]
    public ActionResult<string> LoadJson([FromBody] string json)
    {
        try
        {
            var p = JsonSerializer.Deserialize<Prefs>(json);
            return p?.Theme ?? "light";
        }
        catch (JsonException)
        {
            return BadRequest();
        }
    }

    // BinaryFormatter: eliminar el endpoint o migrar a JSON.
    // Json.NET: TypeNameHandling = TypeNameHandling.None (valor por defecto).
}

public class Prefs { public string Theme { get; set; } }
