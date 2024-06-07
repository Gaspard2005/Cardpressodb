SELECT people.IDPerson, people.IDCard, people.Lastname, people.Firstname, site.Name AS SiteName, department.Name AS DepartmentName, people.IDSAP
FROM people
LEFT JOIN site ON people.Site = site.IDSite
LEFT JOIN department ON people.Department = department.IDDepartment

SELECT * FROM people WHERE IDCard = %s OR IDSAP = %s

INSERT INTO people (IDCard, Lastname, Firstname, Site, Department, IDSAP) 
VALUES (%s, %s, %s, %s, %s, %s)

SELECT * FROM people WHERE IDPerson = %s

UPDATE people SET IDCard = %s, Lastname = %s, Firstname = %s, Site = %s, Department = %s, IDSAP = %s 
WHERE IDPerson = %s

DELETE FROM people WHERE IDPerson = %s