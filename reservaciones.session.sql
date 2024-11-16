create table clientes(
    id_cliente int primary key auto_increment,
    nombre varchar(40),
    correo varchar(40),
    telefono int
);

create table mesas(
    id_mesa int primary key auto_increment,
    capacidad int,
    ocupado boolean
);

create table reservas(
    id_reserva int primary key auto_increment,
    id_cliente int,
    id_mesa int,
    fecha date,
    hora time,
    nPersonas int,
    estado boolean
);



create table administradores(
    id_administrador int primary key auto_increment,
    nombre varchar(40),
    contrasena varchar(40)
);

-- 4
-- 6
insert into mesas(capacidad, ocupado) values(4, false);
insert into mesas(capacidad, ocupado) values(4, false);
insert into mesas(capacidad, ocupado) values(4, false);
insert into mesas(capacidad, ocupado) values(4, false);
insert into mesas(capacidad, ocupado) values(4, false);
insert into mesas(capacidad, ocupado) values(4, false);

-- 2
-- 7
insert into mesas(capacidad, ocupado) values(2, false);
insert into mesas(capacidad, ocupado) values(2, false);
insert into mesas(capacidad, ocupado) values(2, false);
insert into mesas(capacidad, ocupado) values(2, false);
insert into mesas(capacidad, ocupado) values(2, false);
insert into mesas(capacidad, ocupado) values(2, false);
insert into mesas(capacidad, ocupado) values(2, false);


-- 1
-- 2
insert into mesas(capacidad, ocupado) values(1, false);
insert into mesas(capacidad, ocupado) values(1, false);

-- 3
-- 7
insert into mesas(capacidad, ocupado) values(3, false);
insert into mesas(capacidad, ocupado) values(3, false);
insert into mesas(capacidad, ocupado) values(3, false);
insert into mesas(capacidad, ocupado) values(3, false);
insert into mesas(capacidad, ocupado) values(3, false);
insert into mesas(capacidad, ocupado) values(3, false);
insert into mesas(capacidad, ocupado) values(3, false);




SELECT * from clientes;

select * from mesas;

insert into reservas(id_cliente, id_mesa, fecha, hora, nPersonas, estado) values(1, 3, '2021-06-01', '12:00:00', 1, true);

insert into reservas(id_cliente, id_mesa, fecha, hora, nPersonas, estado) values(1, 4, '2024-11-14', '14:00:00', 3, true);



insert into clientes(nombre, correo, telefono) values("Pedro", "pedrito@gmail.com","24443243");

update mesas set mesas.ocupado = true where mesas.id_mesa = 1;

select * from reserva;


insert into administradores(nombre, contrasena) values("admin", "admin");

SELECT * from administradores;


select clientes.nombre, mesas.id_mesa, reservas.fecha, reservas.hora, reservas.nPersonas 
from reservas
left join clientes ON clientes.id_cliente = reservas.id_cliente
left join mesas ON mesas.id_mesa = reservas.id_mesa
where clientes.correo = "pedrito@gmail.com"
order by reservas.fecha desc, reservas.hora desc
;


show databases;