namespace MemberQuery.Builders
{
	using System.Collections.Generic;
	using System.Data.SqlClient;

	using MemberQuery.Models;
	using MemberQuery.Resources;

	public class NewMemberPredictionsBuilder : IBuilder<IEnumerable<NewMemberBalancePrediction>>
	{
		private const string NewMemberPredictionsSql = @"select 
top 1000 NewMemberID, DependentID, BirthYear, State, max(LastCPTCode), CachedBalance, RecommendedBalance, SufficientAmount, ServiceEnd 
from [dbo].[NewMemberBalancePredictions] 
group by NewMemberID, DependentID, BirthYear, State, CachedBalance, RecommendedBalance, SufficientAmount, ServiceEnd
order by RecommendedBalance desc";

		private readonly string connectionString;

		public NewMemberPredictionsBuilder(string connectionString)
		{
			connectionString.CheckIfArgNull("connectionString");
			this.connectionString = connectionString;
		}

		public IEnumerable<NewMemberBalancePrediction> Build()
		{
			using (var connection = new SqlConnection(this.connectionString))
			using (var command = new SqlCommand(NewMemberPredictionsSql, connection))
			{
				connection.Open();

				var reader = command.ExecuteReader();

				while (reader.Read())
				{
					yield return NewMemberBalancePrediction.Factory(reader);
				}
			}
		}
	}
}