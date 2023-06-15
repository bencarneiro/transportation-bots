SELECT 
    transit_agency.agency_name,
    transit_agency.id AS transit_agency_id,
    passenger_miles.passenger_miles,
    spending.operating_expenses,
    (spending.operating_expenses / passenger_miles.passenger_miles) AS cost_per_passenger_mile
FROM 
    transit_agency

LEFT JOIN (
    
    SELECT 
        transit_agency.agency_name,
        transit_agency.id AS transit_agency_id,
        sum(pmt.pmt) AS passenger_miles
    FROM 
        pmt
    LEFT JOIN
        transit_agency
    ON
        transit_agency.id = pmt.transit_agency_id
    WHERE
        pmt.mode_id IN ("CR", "YR")
    GROUP BY
        transit_agency.id, transit_agency.agency_name
    ORDER BY passenger_miles DESC

) AS passenger_miles ON passenger_miles.transit_agency_id = transit_agency.id

LEFT JOIN (

	SELECT 
		transit_agency.agency_name,
		transit_agency.id AS transit_agency_id,
		sum(transit_expense.expense) AS operating_expenses
	FROM 
		transit_expense
	LEFT JOIN
		transit_agency
	ON
		transit_agency.id = transit_expense.transit_agency_id
	WHERE
		transit_expense.mode_id  IN ("CR", "YR")
	AND
		transit_expense.expense_type_id IN ("VO", "VM", "NVM", "GA")
	GROUP BY
		transit_agency.id, transit_agency.agency_name
	ORDER BY operating_expenses DESC

) 
AS spending ON spending.transit_agency_id = transit_agency.id
	
WHERE 
    passenger_miles.passenger_miles IS NOT NULL
AND 
    passenger_miles.passenger_miles > 0
AND 
    spending.operating_expenses IS NOT NULL
AND 
    spending.operating_expenses > 0
ORDER BY 
    cost_per_passenger_mile ASC;