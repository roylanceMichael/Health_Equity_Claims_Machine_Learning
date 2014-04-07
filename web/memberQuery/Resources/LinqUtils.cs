namespace MemberQuery.Resources
{
	using System;
	using System.Collections.Generic;
	using System.Linq;

	// http://stackoverflow.com/questions/2253874/linq-equivalent-for-standard-deviation - thank you!
	public static class LinqUtils
	{
		public static double StdDev(this IEnumerable<double> values)
		{
			double ret = 0;
			int count = values.Count();
			if (count > 1)
			{
				// Compute the Average
				double avg = values.Average();

				// Perform the Sum of (value-avg)^2
				double sum = values.Sum(d => (d - avg) * (d - avg));

				// Put it all together
				ret = Math.Sqrt(sum / count);
			}

			return ret;
		}
	}
}