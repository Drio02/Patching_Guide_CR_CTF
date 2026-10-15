using Microsoft.Data.SqlClient;

public class UserRepo
{
    private readonly SqlConnection _conn;
    public UserRepo(SqlConnection conn) => _conn = conn;

    // Vuln 1: interpolacion de strings en SqlCommand
    public bool Login(string user, string pass)
    {
        var cmd = new SqlCommand(
            $"SELECT COUNT(*) FROM Users WHERE Username = '{user}' AND Password = '{pass}'", _conn);
        return (int)cmd.ExecuteScalar() > 0;   // payload user: admin' --
    }

    // Vuln 2: Entity Framework con FromSqlRaw + concatenacion
    // db.Notes.FromSqlRaw("SELECT * FROM Notes WHERE Owner = '" + owner + "'")
}
