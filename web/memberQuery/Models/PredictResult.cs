namespace MemberQuery.Models
{
	using System;
	using System.Data.SqlClient;

	public class PredictResult
	{
		public string Path { get; set; }

		public double? GoldAmount { get; set; }

		public double? ExpectedAmount { get; set; }

		public double? TrainAmount { get; set; }

		public double? TrainLowest { get; set; }

		public double? TrainHighest { get; set; }

		public double? GoldExpectedVariation
		{
			get
			{
				if (this.GoldAmount.HasValue && this.ExpectedAmount.HasValue)
				{
					return Math.Round(this.GoldAmount.Value / this.ExpectedAmount.Value, 2);
				}

				return null;
			}
		}

		public double GoldExpectedVariance { get; set; }

		public double GoldExpectedStandardDeviation { get; set; }

		public static PredictResult Factory(SqlDataReader reader)
		{
			return new PredictResult
				            {
											Path = SafeToString(reader.GetString(0)),
											GoldAmount = SafeToDouble(reader.GetString(1)),
											ExpectedAmount = SafeToDouble(reader.GetString(2)),
											TrainAmount = SafeToDouble(reader.GetString(3)),
											TrainLowest = SafeToDouble(reader.GetString(4)),
											TrainHighest = SafeToDouble(reader.GetString(5))
				            };
		}

		private static double? SafeToDouble(string value)
		{
			double doubleValue;
			if (double.TryParse(value, out doubleValue))
			{
				return Math.Round(doubleValue, 2);
			}
			return null;
		}

		private static string SafeToString(object value)
		{
			return value == null ? string.Empty : value.ToString();
		}
	}
}