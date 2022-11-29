# gf-cost-compare

## Overview
Millions of people in the USA suffer from celiac disease or other medically diagnosed gluten intolerances 
and have to pay on average hundreds of dollars more for groceries each year than people without these food requirements. 
The US tax code allows writing off gluten-free food that is "in excess of the cost of the gluten containing food 
that you are replacing", however this is a difficult task since people with these conditions are not replacing any 
food, but simply buying their groceries. This process would benefit from a streamlined way to find comparable 
non gluten-free items and show the amount one may write off for the gluten-free item.

## Kroger API
This is a client that interacts with the Kroger Location and Product APIs and returns relevant data given a 
zip code and generic name e.g. 'bread', 'pasta', 'flour', 'oats', etc. The relevant data can include the minimum priced
product, a list of products, or the product price per weight.
