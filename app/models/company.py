from app import mysql


def get_companies():
    cur = mysql.connect().cursor()

    query = "SELECT * FROM company_profiles"
    cur.execute(query)
    companies = cur.fetchall()
    cur.close()

    return companies

def get_detail_company(company_name):
    cur = mysql.connect().cursor()
    query = "SELECT * FROM company_profiles where company_name LIKE %s"
    cur.execute(query, (company_name))
    companies = cur.fetchall()
    cur.close()

    return companies

def get_company_by_industry(industry):
    cur = mysql.connect().cursor()
    query = "SELECT * FROM company_profiles where business = %s"
    cur.execute(query, (industry))
    companies = cur.fetchall()
    cur.close()

    return companies

def get_company_by_revenue(revenue):
    cur = mysql.connect().cursor()
    query = "SELECT * FROM company_profiles where revenue >= %s"
    cur.execute(query, (revenue))
    companies = cur.fetchall()
    cur.close()

    return companies