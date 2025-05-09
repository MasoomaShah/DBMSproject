from configparser import ConfigParser

import psycopg2
from flask import redirect, request,flash,url_for,redirect
# Here in this file I tried to create GUI using tkinter
# The GUI created here contain different fields to insert record in the
import psycopg2
def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    
    return db
def fetch_data():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM pakistan_census_data")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return columns, rows
    except Exception as e:
        print("Database error:", e)
        return [], []

def Delete_rows():
    selected_ids = request.form.getlist('delete_ids')  # Gets all selected checkboxes
    if not selected_ids:

        flash("No rows selected.", "error")
        return redirect(url_for('views.home'))
    
    try:
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for pk in selected_ids:
            cur.execute("DELETE FROM pakistan_census_data WHERE census_id= %s", (pk,))
        conn.commit()
        cur.close()
        conn.close()
        # flash instead for meaage box that was takinter
        flash("Deleted successfully",category="success")

    except Exception as e:
        flash(f"Error :{str(e)}",category="error")
    # selected_ids = request.form.getlist('delete_ids')  # Gets all selected checkboxes

    # if not selected_ids:
    #     flash("No rows selected.", category="error")
    #     return redirect(url_for('views.home'))
    
    # try:
    #     params = config()
    #     conn = psycopg2.connect(**params)
    #     cur = conn.cursor()
    #     for pk in selected_ids:
    #         cur.execute("DELETE FROM pakistan_census_data WHERE census_id= %s", (pk,))
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #     # flash instead for meaage box that was takinter
    #     flash("Deleted successfully",category="success")

    # except Exception as e:
    #     flash(f"Error :{str(e)}",category="error")
   


# def update_record():
#     try:
#         data = request.form

#         PROVINCE = data['PROVINCE']
#         DIVISION = data['DIVISION']
#         DISTRICT = data['DISTRICT']
#         SUB_DIVISION = data['SUB_DIVISION']
#         AREA_sq_km = data['AREA_sq_km']
#         ALL_SEXES_RURAL = data['ALL_SEXES_RURAL']
#         MALE_RURAL = data['MALE_RURAL']
#         FEMALE_RURAL = data['FEMALE_RURAL']
#         SEX_RATIO_RURAL = data['SEX_RATIO_RURAL']
#         AVG_HOUSEHOLD_SIZE_RURAL = data['AVG_HOUSEHOLD_SIZE_RURAL']
#         POPULATION_1998_RURAL = data['POPULATION_1998_RURAL']
#         ANNUAL_GROWTH_RATE_RURAL = data['ANNUAL_GROWTH_RATE_RURAL']
#         ALL_SEXES_URBAN = data['ALL_SEXES_URBAN']
#         MALE_URBAN = data['MALE_URBAN']
#         FEMALE_URBAN = data['FEMALE_URBAN']
#         SEX_RATIO_URBAN = data['SEX_RATIO_URBAN']
#         AVG_HOUSEHOLD_SIZE_URBAN = data['AVG_HOUSEHOLD_SIZE_URBAN']
#         POPULATION_1998_URBAN = data['POPULATION_1998_URBAN']
#         ANNUAL_GROWTH_RATE_URBAN = data['ANNUAL_GROWTH_RATE_URBAN']
#         CENSUS_ID = data['census_id']  # you'll need this passed in hidden input

#         params = config()
#         conn = psycopg2.connect(**params)
#         cur = conn.cursor()

#         cur.execute("""
#             UPDATE pakistan_census_data SET 
#                 PROVINCE = %s,
#                 DIVISION = %s,
#                 DISTRICT = %s,
#                 SUB_DIVISION = %s,
#                 AREA_sq_km = %s,
#                 ALL_SEXES_RURAL = %s,
#                 MALE_RURAL = %s,
#                 FEMALE_RURAL = %s,
#                 SEX_RATIO_RURAL = %s,
#                 AVG_HOUSEHOLD_SIZE_RURAL = %s,
#                 POPULATION_1998_RURAL = %s,
#                 ANNUAL_GROWTH_RATE_RURAL = %s,
#                 ALL_SEXES_URBAN = %s,
#                 MALE_URBAN = %s,
#                 FEMALE_URBAN = %s,
#                 SEX_RATIO_URBAN = %s,
#                 AVG_HOUSEHOLD_SIZE_URBAN = %s,
#                 POPULATION_1998_URBAN = %s,
#                 ANNUAL_GROWTH_RATE_URBAN = %s
#             WHERE census_id = %s
#         """, (
#             PROVINCE, DIVISION, DISTRICT, SUB_DIVISION, AREA_sq_km,
#             ALL_SEXES_RURAL, MALE_RURAL, FEMALE_RURAL, SEX_RATIO_RURAL,
#             AVG_HOUSEHOLD_SIZE_RURAL, POPULATION_1998_RURAL, ANNUAL_GROWTH_RATE_RURAL,
#             ALL_SEXES_URBAN, MALE_URBAN, FEMALE_URBAN, SEX_RATIO_URBAN,
#             AVG_HOUSEHOLD_SIZE_URBAN, POPULATION_1998_URBAN, ANNUAL_GROWTH_RATE_URBAN,
#             CENSUS_ID
#         ))

#         conn.commit()
#         cur.close()
#         conn.close()

#         flash("Record updated successfully!", category='success')
#     except Exception as e:
#         flash(f"Error updating record: {e}", category='error')
# def edit_row(census_id):
#     params = config()
#     conn = psycopg2.connect(**params)
#     cur = conn.cursor()

#     if request.method == "POST":
#         return update_record()

#     # GET request: show form
#     cur.execute("SELECT * FROM pakistan_census_data WHERE census_id = %s", (census_id,))
#     record = cur.fetchone()
#     columns = [desc[0] for desc in cur.description]
#     cur.close()
#     conn.close()







