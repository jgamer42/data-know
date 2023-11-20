/*NOMBRE Y APELLIDO DE LOS EMPLEADOS*/
SELECT NOMBRE,apellido,salario FROM EMPLEADO;

/* EMPLEADOS QUE GANAN MAS DE 4000000*/
SELECT NOMBRE,apellido,salario FROM EMPLEADO 
    WHERE SALARIO >= 4000000;

/*CUENTA DE EMPLEADOS POR SEXO*/
SELECT SEXO, COUNT(*) FROM EMPLEADO 
    GROUP BY sexo

/*EMPLEADOS QUE NO HAN SOLICITADO VACACIONES*/
SELECT * FROM EMPLEADO 
    WHERE ID NOT IN (SELECT id_emp FROM VACACIONES);

/*empleados con vacaciones y dias promedio*/
SELECT emp.nombre,emp.APELLIDO, avg(vac.cantidad_dias) 
FROM EMPLEADO EMP 
inner JOIN VACACIONES VAC 
    ON EMP.ID = VAC.id_emp 
GROUP BY Emp.id;

/*empleado con el promedio mas alto de dias solicitados*/
SELECT emp.nombre,emp.APELLIDO, sum(vac.cantidad_dias) 
FROM EMPLEADO EMP 
inner JOIN VACACIONES VAC 
    ON EMP.ID = VAC.id_emp 
GROUP BY Emp.id 
order by  avg(vac.cantidad_dias) desc limit 1;
/*dias rechazados y aprobados por empleado*/
SELECT 
    e.nombre,
    COALESCE(SUM(CASE WHEN v.estado = 'A' THEN v.cantidad_dias ELSE 0 END), 0) as aprobados,
    COALESCE(SUM(CASE WHEN v.estado = 'R' THEN v.cantidad_dias ELSE 0 END), 0) as rechazados
FROM empleado e
    LEFT JOIN vacaciones v ON e.id = v.id_emp
GROUP BY v.id_emp;