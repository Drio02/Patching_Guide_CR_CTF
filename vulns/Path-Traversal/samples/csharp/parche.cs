using Microsoft.AspNetCore.Mvc;

[ApiController]
public class FilesController : ControllerBase
{
    private static readonly string BaseDir =
        Path.GetFullPath("/srv/notes") + Path.DirectorySeparatorChar;

    // Patch: GetFullPath resuelve ".." y la verificacion de prefijo incluye el separador
    [HttpGet("/download")]
    public IActionResult Download(string file)
    {
        var full = Path.GetFullPath(Path.Combine(BaseDir, file));
        if (!full.StartsWith(BaseDir, StringComparison.Ordinal))
            return Forbid();
        return PhysicalFile(full, "application/octet-stream");
    }

    // Alternativa: solo nombres simples
    // if (file != Path.GetFileName(file)) return BadRequest();
}
