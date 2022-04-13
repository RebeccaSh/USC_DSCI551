use sakila;
/*1) Find out how many films are rated ‘PG-13’ and last between 100 and 200 minutes.*/
SELECT COUNT(*) FROM sakila.film where rating = 'PG-13'AND (length between 100 and 200);

/*2) Find first and last names of actors whose 2nd to the last letter of last name is ‘i’.*/
SELECT first_name, last_name FROM sakila.actor where substring(last_name,length(last_name)-1,1) = 'i';
/*3) Find the title and length of the longest films.*/
SELECT title,length FROM sakila.film WHERE length = (SELECT MAX(length) FROM sakila.film_list);

/*4) Find out how many films there are in each category. Output category name and the number of films in the category.*/

SELECT category.name, COUNT(film_id) from sakila.film_category right JOIN sakila.category on film_category.category_id = category.category_id group by category.name ;

/*5) Find ids of customers who have rented films at least 40 times. Return the same ids only once.*/

SELECT distinct(customer_id) FROM sakila.rental group by customer_id having  COUNT(customer_id) >= 40  ;

/*6) Find first and last names of customers whose total payment exceeds $200.*/
SELECT first_name, last_name from sakila.customer where customer_id in (SELECT customer_id from sakila.payment group by customer_id having SUM(amount) >200);


/*7) Find first and last names of actors who have never played in films rated R.*/
SELECT first_name, last_name from sakila.actor where actor_id not in (SELECT actor_id from sakila.film_actor where film_id  in (SELECT film_id FROM sakila.film where rating = 'R'));


/*8) Find out how many films are not available in the inventory.*/
SELECT count(*) from sakila.film where  film_id not in (SELECT film_id FROM sakila.inventory);

/*9) Find out how many actors who have the same first name but a different last name with another actor.*/
SELECT c.first_name ,c.last_name FROM sakila.actor as c where c.first_name in (SELECT first_name FROM sakila.customer as where a.first_name = b.first_name );

SELECT c.last_name, c.first_name
FROM sakila.actor as c WHERE c.last_name not IN (SELECT a.last_name FROM sakila.actor as a inner join (SELECT first_name FROM sakila.actor)AS b on a.first_name = b.first_name );
 
 SELECT c.first_name ,c.last_name
FROM sakila.customer as c WHERE c.first_name in (SELECT first_name FROM sakila.customer)AS b on a.first_name = b.first_name ) join c.last_name not IN (SELECT a.last_name FROM sakila.customer as a);
   
   
SELECT
    t1.first_name,
    t1.last_name
FROM sakila.actor as  t1
     JOIN actor t2 ON t1.first_name = t2.first_name where t1.last_name != t2.last_name;
  
   
SELECT a.last_name FROM sakila.customer as a inner join (SELECT last_name FROM sakila.customer GROUP BY last_name HAVING COUNT (last_name)> 1);
   /*10) Show the first name, last name, and city of the customers whose first name is either Jamie,Jessie, or Leslie. Order the result by first name.*/

SELECT customer.first_name, customer.last_name, city.city FROM customer JOIN address ON customer.address_id = address.address_id JOIN city ON address.city_id = city.city_id where first_name = 'Jamie' or first_name = 'Leslie' or first_name = 'Jessie' order by first_name;

   