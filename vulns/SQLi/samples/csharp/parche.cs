using Microsoft.Data.SqlClient;

public class UserRepo
{
    private readonly SqlConnection _conn;
    public UserRepo(SqlConnection conn) => _conn = conn;

    // Patch 1: parametros con nombre
    public bool Login(string user, string pass)
    {
        using var cmd = new SqlCommand(
            "SELECT COUNT(*) FROM Users WHERE Username = @u AND Password = @p", _conn);
        cmd.Parameters.AddWithValue("@u", user);
        cmd.Parameters.AddWithValue("@p", pass);
        return (int)cmd.ExecuteScalar() > 0;
    }

    // Patch 2: Entity Framework
    // FromSqlInterpolated convierte cada {x} en un parametro (FromSqlRaw NO)
    // db.Notes.FromSqlInterpolated($"SELECT * FROM Notes WHERE Owner = {owner}")
    // o mejor LINQ:  db.Notes.Where(n => n.Owner == owner)
}
