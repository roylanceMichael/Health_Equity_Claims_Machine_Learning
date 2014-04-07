namespace MemberQuery.Models
{
	using System;
	using System.Data.SqlClient;

	public class NewMemberBalancePrediction
	{
		public int NewMemberId { get; set; }

		public int DependentId { get; set; }

		public int BirthYear { get; set; }

		public string State { get; set; }

		public string LastCptCode { get; set; }

		public string CachedBalance { get; set; }

		public double RecommendedBalance { get; set; }

		public int SufficientAmount { get; set; }

		public DateTime ServiceEnd { get; set; }

		public static NewMemberBalancePrediction Factory(SqlDataReader reader)
		{
			var newMemberId = reader.GetInt32(0);
			var dependentId = reader.GetInt32(1);
			var birthYear = reader.GetInt32(2);
			var state = reader.GetString(3);
			var lastCptCode = reader.GetString(4);
			var cachedBalance = reader.GetString(5);
			var recommendedBalance = reader.GetValue(6);

			double d;
			double.TryParse(recommendedBalance == null ? "0" : recommendedBalance.ToString(), out d);
			var sufficientAmount = reader.GetInt32(7);
			var serviceEnd = reader.GetDateTime(8);

			return new NewMemberBalancePrediction
				       {
					       NewMemberId = newMemberId,
								 DependentId = dependentId,
								 BirthYear = birthYear,
								 State = state,
								 LastCptCode = lastCptCode,
								 CachedBalance = cachedBalance,
								 RecommendedBalance = Math.Round(d, 2),
								 SufficientAmount = sufficientAmount,
								 ServiceEnd = serviceEnd
				       };
		}
	}
}