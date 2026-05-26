#include <sqlite3.h>
#include <stdio.h>
#include <string.h>

// SQLite C API

/*
    sprintf + sqlite3_exec
*/

int login_vuln(sqlite3 *db, const char *user, const char *pass) {
    char query[512];
    sprintf(query,
        "SELECT * FROM users WHERE username='%s' AND password='%s'",
        user, pass);
    return sqlite3_exec(db, query, NULL, NULL, NULL)
    // Payload user: admin' --
}

// libpq (PostgresSQL)

#include <libpq-fe.h>

PGresult *find_user_vuln(PGconn *conn, const char *name) {
    char query[1024];
    snprintf(query, sizeof(query),
        "SELECT id, email FROM users WHERE name = '%s'", name);
    return PQexec(conn, query);
}