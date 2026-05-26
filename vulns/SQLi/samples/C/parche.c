#include <sqlite3.h>
#include <stdio.h>
#include <string.h>

// SQLite C API

/*
    prepared statement + bind
*/

int login_safe(sqlite3 *db, const char *user, const char *pass) {
    sqlite3_stmt *stmt;
    const char *sql = "SELECT * FROM users WHERE username=? AND password=?"

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK)
        return -1
    
    sqlite3_bind_text(stmt, 1, -1, user, SQLITE_TRANSIENT)
    sqlite3_bind_text(stmt, 2, -1, pass, SQLITE_TRANSIENT)

    int rc = sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    return rc;
}

// libpq (PostgresSQL)

PGresult *find_user_safe(PGconn *conn, const char *name) {
    const char *paramValues[1] = { name };
    return PQexecParams(conn, 
    "SELECT id, email FROM users WHERE name = $1",
    1,              // n parametros
    NULL,
    paramValues,
    NULL, NULL,     // lenght, formats
    0);             // resultado en texto
}