import java.sql.*;

public class UserDao {
    private final Connection conn;
    public UserDao(Connection conn) { this.conn = conn; }

    // Patch 1: PreparedStatement
    public boolean login(String user, String pass) throws SQLException {
        try (PreparedStatement ps = conn.prepareStatement(
                "SELECT id FROM users WHERE username = ? AND password = ?")) {
            ps.setString(1, user);
            ps.setString(2, pass);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }

    // Patch 2: PreparedStatement en vez de String.format
    public ResultSet notesOf(String owner) throws SQLException {
        PreparedStatement ps = conn.prepareStatement("SELECT * FROM notes WHERE owner = ?");
        ps.setString(1, owner);
        return ps.executeQuery();
    }

    // Patch 3: JPA con parametro con nombre
    // em.createQuery("FROM Note n WHERE n.owner = :owner", Note.class)
    //   .setParameter("owner", owner).getResultList();
}
