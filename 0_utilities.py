# Functions for salary conversion
# Subfunctions called by main function
def hour_to_year(min, max, hours_a_week):
  # Conversion from salary in currency/hour to currency/year.
  # Can change the number of working hours/week.
  weeks_per_year=52
  min_converted = min * hours_a_week * weeks_per_year
  max_converted = max * hours_a_week * weeks_per_year
  return min_converted, max_converted

def year_to_month(min, max):
  # Conversion from salary in currency/year to currency/month.
  months_per_year=12
  min_converted = min / months_per_year
  max_converted = max / months_per_year
  return min_converted, max_converted

def month_to_year(min, max):
  # Conversion from salary in currency/month to currency/year.
  months_per_year=12
  min_converted = min * months_per_year
  max_converted = max * months_per_year
  return min_converted, max_converted

def year_to_hour(min, max, hours_a_week):
  # Conversion from salary in currency/year to currency/hour.
  weeks_per_year=52
  min_converted = min / (weeks_per_year * hours_a_week )
  max_converted = max / (weeks_per_year * hours_a_week )
  return min_converted, max_converted

# Main function
def salary_conversion(min_sal, max_sal, unit_in, unit_out, hours_a_week):
  """
  Function receives a min, max salary and a unit_in and unit_out (h: hour, m: month, y:year)
  and returns the converted salary.
  Supported conversions: h->m, h->y, m->y. If unit_in == unit_out, returns inputs. 
  Could add more if needed, just update the routes dictionary below.
  Arguments:
    min_sal: minimum salary
    max_sal: maximum salary
    unit_in: unit of the salary (hour, month, year)
    unit_out: desired unit of the salary (hour, month, year)
    hours_a_week: number of hours to consider worked per week. 
  Returns:
    converted_salary: converted salary: min_converted, max_converted
  """
  # Error control.
  if min_sal > max_sal:
      raise ValueError("Minimum salary cannot be greater than maximum salary.")
  
  # Ensure argument values for unit in and out are in lower case, before comparisons.
  unit_in  = unit_in.lower()
  unit_out = unit_out.lower()

  # If no unit change is needed:
  if unit_in == unit_out:
      return min_sal, max_sal

  # If unit change is needed: these are the supported pipelines, 
  # each option maps to the correspondent subfunctions.
  routes = {
        ('hour', 'year'): [
            lambda mn, mx: hour_to_year(mn, mx, hours_a_week)
        ],
        ('hour', 'month'): [
            lambda mn, mx: hour_to_year(mn, mx, hours_a_week),
            year_to_month
        ],
        ('month', 'year'): [
            month_to_year
        ],
        ('year', 'hour'): [
            lambda mn, mx: year_to_hour(mn, mx, hours_a_week)
        ],
        ('month', 'hour'): [
            month_to_year,                             # month -> year
            lambda mn, mx: year_to_hour(mn, mx, hours_a_week), # year -> hour
        ],
    }

  try:
      for function in routes[(unit_in, unit_out)]:
          min_sal, max_sal = function(min_sal, max_sal)
      return min_sal, max_sal
  except KeyError:
      raise ValueError(f"Unsupported conversion {unit_in!r} -> {unit_out!r}")