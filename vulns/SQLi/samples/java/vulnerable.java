import java.sql.*;

public class UserDao {
    private final Connection conn;
    public UserDao(Connection conn) { this.conn = conn; }

    // Vuln 1: Statement + concatenacion
    public boolean login(String user, String pass) throws SQLException {
        Statement st = conn.createStatement();
        ResultSet rs = st.executeQuery(
            "SELECT id FROM users WHERE username = '" + user + "' AND password = '" + pass + "'");
        return rs.next();   // payload user: admin' --
    }

    // Vuln 2: String.format tambien es concatenacion
    public ResultSet notesOf(String owner) throws SQLException {
        return conn.createStatement().executeQuery(
            String.format("SELECT * FROM notes WHERE owner = '%s'", owner));
    }

    // Vuln 3: JPA/Hibernate con JPQL concatenado
    // em.createQuery("FROM Note n WHERE n.owner = '" + owner + "'").getResultList();
}
