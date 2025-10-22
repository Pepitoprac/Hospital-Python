BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "area" (
	"id"	INTEGER,
	"descripcion"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "especialidad" (
	"id"	INTEGER,
	"area_id"	INTEGER NOT NULL,
	"nombre"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("area_id") REFERENCES "area"("id")
);
CREATE TABLE IF NOT EXISTS "historia_clinica" (
	"id"	INTEGER,
	"paciente_id"	INTEGER NOT NULL,
	"medico_id"	INTEGER NOT NULL,
	"area_id"	INTEGER NOT NULL,
	"fecha"	TEXT NOT NULL,
	"hora"	TEXT NOT NULL,
	"detalles_sintomas"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("area_id") REFERENCES "area"("id"),
	FOREIGN KEY("medico_id") REFERENCES "medico"("id"),
	FOREIGN KEY("paciente_id") REFERENCES "paciente"("id")
);
CREATE TABLE IF NOT EXISTS "medico" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"matricula"	TEXT NOT NULL,
	"especialidad_id"	INTEGER,
	PRIMARY KEY("id","matricula"),
	FOREIGN KEY("especialidad_id") REFERENCES "especialidad"("id")
);
CREATE TABLE IF NOT EXISTS "paciente" (
	"id"	INTEGER,
	"dni"	TEXT NOT NULL UNIQUE,
	"nombre"	TEXT NOT NULL,
	"fechaNacimiento"	TEXT,
	PRIMARY KEY("id","dni")
);
CREATE TABLE IF NOT EXISTS "turno" (
	"id"	INTEGER,
	"paciente_id"	INTEGER NOT NULL,
	"medico_id"	INTEGER NOT NULL,
	"fecha"	TEXT NOT NULL,
	"hora"	TEXT NOT NULL,
	"urgencia"	INTEGER NOT NULL CHECK("urgencia" BETWEEN 1 AND 4),
	"area_id"	INTEGER NOT NULL,
	"matriculamedico"	INTEGER NOT NULL,
	"dnipaciente"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("area_id") REFERENCES "area"("id"),
	FOREIGN KEY("dnipaciente") REFERENCES "paciente"("dni"),
	FOREIGN KEY("matriculamedico") REFERENCES "medico"("matricula"),
	FOREIGN KEY("medico_id") REFERENCES "medico"("id"),
	FOREIGN KEY("paciente_id") REFERENCES "paciente"("id")
);
CREATE TABLE IF NOT EXISTS "usuario" (
	"id"	INTEGER,
	"nombre"	TEXT,
	"contrasena"	TEXT,
	"rol"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "area" VALUES (1,'Pediatria');
INSERT INTO "area" VALUES (2,'Cardiologia');
INSERT INTO "area" VALUES (3,'Neurologia');
INSERT INTO "area" VALUES (4,'Oncologia');
INSERT INTO "area" VALUES (5,'Ginecologia');
INSERT INTO "area" VALUES (6,'Traumatologia');
INSERT INTO "area" VALUES (7,'Dermatologia');
INSERT INTO "area" VALUES (8,'Oftalmologia');
INSERT INTO "area" VALUES (9,'Urologia');
INSERT INTO "area" VALUES (10,'Psiquiatria');
INSERT INTO "especialidad" VALUES (1,1,'Pediatra');
INSERT INTO "especialidad" VALUES (2,2,'Cardiologo');
INSERT INTO "especialidad" VALUES (3,3,'Neurologo');
INSERT INTO "especialidad" VALUES (4,4,'Oncologo');
INSERT INTO "especialidad" VALUES (5,5,'Ginecologo');
INSERT INTO "especialidad" VALUES (6,6,'Traumatologo');
INSERT INTO "especialidad" VALUES (7,7,'Dermatologo');
INSERT INTO "especialidad" VALUES (8,8,'Oftalmologo');
INSERT INTO "especialidad" VALUES (9,9,'Urologo');
INSERT INTO "especialidad" VALUES (10,10,'Psiquiatra');
INSERT INTO "historia_clinica" VALUES (1,1,1,1,'2025-01-05','10:30','Dolor abdominal');
INSERT INTO "historia_clinica" VALUES (2,2,2,2,'2025-02-10','09:00','Dolor en el pecho');
INSERT INTO "historia_clinica" VALUES (3,3,3,3,'2025-03-12','11:15','Dolores de cabeza');
INSERT INTO "historia_clinica" VALUES (4,4,4,4,'2025-03-20','14:00','Fatiga constante');
INSERT INTO "historia_clinica" VALUES (5,5,5,5,'2025-04-02','15:45','Dolor pelvico');
INSERT INTO "historia_clinica" VALUES (6,6,6,6,'2025-04-10','16:30','Fractura de brazo');
INSERT INTO "historia_clinica" VALUES (7,7,7,7,'2025-05-01','12:20','Erupcion en la piel');
INSERT INTO "historia_clinica" VALUES (8,8,8,8,'2025-05-15','13:10','Problemas de vision');
INSERT INTO "historia_clinica" VALUES (9,9,9,9,'2025-06-01','08:50','Dolor al orinar');
INSERT INTO "historia_clinica" VALUES (10,10,10,10,'2025-06-18','17:00','Ansiedad y estres');
INSERT INTO "medico" VALUES (1,'Dr. Juan Lopez','MAT1001',1);
INSERT INTO "medico" VALUES (2,'Dra. Ana Garcia','MAT1002',2);
INSERT INTO "medico" VALUES (3,'Dr. Carlos Torres','MAT1003',3);
INSERT INTO "medico" VALUES (4,'Dra. Laura Perez','MAT1004',4);
INSERT INTO "medico" VALUES (5,'Dr. Pedro Fernandez','MAT1005',5);
INSERT INTO "medico" VALUES (6,'Dra. Sofia Romero','MAT1006',6);
INSERT INTO "medico" VALUES (7,'Dr. Martin Gonzalez','MAT1007',7);
INSERT INTO "medico" VALUES (8,'Dra. Camila Suarez','MAT1008',8);
INSERT INTO "medico" VALUES (9,'Dr. Diego Castro','MAT1009',9);
INSERT INTO "medico" VALUES (10,'Dra. Lucia Herrera','MAT1010',10);
INSERT INTO "medico" VALUES (11,'Lucas Valebzuela','1ABC',2);
INSERT INTO "medico" VALUES (12,'franco','2ABC',5);
INSERT INTO "paciente" VALUES (1,'1234','Franco','20070521');
INSERT INTO "paciente" VALUES (2,'30222333','Maria Lopez','1985-08-15');
INSERT INTO "paciente" VALUES (3,'30333444','Carlos Gomez','1978-02-22');
INSERT INTO "paciente" VALUES (4,'30444555','Ana Torres','2000-11-30');
INSERT INTO "paciente" VALUES (5,'30555666','Pedro Ramirez','1995-04-18');
INSERT INTO "paciente" VALUES (6,'30666777','Lucia Fernandez','1982-06-25');
INSERT INTO "paciente" VALUES (7,'30777888','Diego Martinez','1998-01-12');
INSERT INTO "paciente" VALUES (8,'30888999','Sofia Alvarez','1992-07-07');
INSERT INTO "paciente" VALUES (9,'30999000','Martina Sanchez','1987-12-09');
INSERT INTO "paciente" VALUES (10,'31000111','Federico Castro','1993-09-14');
INSERT INTO "turno" VALUES (1,1,1,'2025-09-17','16:32',1,1,'MAT1001',1234);
INSERT INTO "turno" VALUES (2,9,1,'2025-09-20','12:55',1,5,'MAT1001',30999000);
INSERT INTO "turno" VALUES (3,2,3,'111111111111111','111111111',1,3,'MAT1003',30222333);
INSERT INTO "usuario" VALUES (1,'lucas','1234','ADMIN');
INSERT INTO "usuario" VALUES (2,'juanp','clave123','Recepcionista');
INSERT INTO "usuario" VALUES (3,'mariaf','pass321','Recepcionista');
INSERT INTO "usuario" VALUES (4,'sofia','sofia2024','Medico');
INSERT INTO "usuario" VALUES (5,'carlos','car123','Medico');
INSERT INTO "usuario" VALUES (6,'ana','ana456','Medico');
INSERT INTO "usuario" VALUES (7,'martin','martin789','Medico');
INSERT INTO "usuario" VALUES (8,'lucas','lucas321','Medico');
INSERT INTO "usuario" VALUES (9,'fernando','ferpass','Medico');
INSERT INTO "usuario" VALUES (10,'camila','cami123','Recepcionista');
INSERT INTO "usuario" VALUES (11,'fran','fran','Admin');
INSERT INTO "usuario" VALUES (12,'diego','diwgo','ADMIN');
INSERT INTO "usuario" VALUES (13,'diego','diego','admin');
COMMIT;
