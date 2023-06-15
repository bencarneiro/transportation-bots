SELECT 
    transit_agency.agency_name,
    transit_agency.id AS transit_agency_id,
    riders.total_riders,
    spending.operating_expenses,
    (spending.operating_expenses / riders.total_riders) AS cost_per_trip
FROM 
    transit_agency

LEFT JOIN (
    
    SELECT 
        transit_agency.agency_name,
        transit_agency.id AS transit_agency_id,
        sum(upt.upt) AS total_riders
    FROM 
        upt
    LEFT JOIN
        transit_agency
    ON
        transit_agency.id = upt.transit_agency_id
    WHERE
        upt.mode_id IN ("CR", "YR")
    GROUP BY
        transit_agency.id, transit_agency.agency_name
    ORDER BY total_riders DESC

) AS riders ON riders.transit_agency_id = transit_agency.id

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
    riders.total_riders IS NOT NULL
AND 
    riders.total_riders > 0
AND 
    spending.operating_expenses IS NOT NULL
AND 
    spending.operating_expenses > 0
ORDER BY 
    cost_per_trip ASC;