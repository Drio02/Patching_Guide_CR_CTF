#include <sqlite3.h>
#include <libpq-fe.h>
#include <stdio.h>
#include <string.h>

// SQLite C API

/*
    prepared statement + bind
*/

int login_safe(sqlite3 *db, const char *user, const char *pass) {
    sqlite3_stmt *stmt;
    const char *sql = "SELECT * FROM users WHERE username=? AND password=?";

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK)
        return -1;

    // sqlite3_bind_text(stmt, indice, valor, longitud, destructor)
    sqlite3_bind_text(stmt, 1, user, -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, pass, -1, SQLITE_TRANSIENT);

    int rc = sqlite3_step(stmt);    // SQLITE_ROW si las credenciales son validas
    sqlite3_finalize(stmt);
    return rc == SQLITE_ROW;
}

// libpq (PostgreSQL)

PGresult *find_user_safe(PGconn *conn, const char *name) {
    const char *paramValues[1] = { name };
    return PQexecParams(conn,
    "SELECT id, email FROM users WHERE name = $1",
    1,              // n parametros
    NULL,           // tipos (los infiere el servidor)
    paramValues,
    NULL, NULL,     // lengths, formats
    0);             // resultado en texto
}
