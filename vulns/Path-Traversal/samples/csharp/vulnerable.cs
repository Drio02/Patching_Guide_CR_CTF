using Microsoft.AspNetCore.Mvc;

[ApiController]
public class FilesController : ControllerBase
{
    private const string BaseDir = "/srv/notes";

    // Vuln 1: Path.Combine devuelve el segundo argumento si es absoluto
    [HttpGet("/download")]
    public IActionResult Download(string file)
    {
        var path = Path.Combine(BaseDir, file);     // ?file=/etc/passwd o ../../etc/passwd
        return PhysicalFile(path, "application/octet-stream");
    }
}
