namespace MemberQuery.Models
{
	using System.Data.SqlClient;

	public class EmissionRecord
	{
		public string CptCode { get; set; }

		public double TotalAmount { get; set; }
 
		public double Probability { get; set; }

		public static EmissionRecord Factory(SqlDataReader dataReader)
		{
			double totalAmount;
			double probability;

			if (!double.TryParse(dataReader.GetString(1), out totalAmount))
			{
				totalAmount = 0;
			}

			if (!double.TryParse(dataReader.GetString(2), out probability))
			{
				probability = 0;
			}

			return new EmissionRecord
				       {
					       CptCode = dataReader.GetString(0),
								 TotalAmount = totalAmount,
								 Probability = probability
				       };
		}
	}
}