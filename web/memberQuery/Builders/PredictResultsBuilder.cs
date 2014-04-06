namespace MemberQuery.Builders
{
	using System.Collections.Generic;
	using System.Data.SqlClient;

	using MemberQuery.Models;

	public class PredictResultsBuilder : IBuilder<IEnumerable<PredictResult>>
	{
		private const string PredictSqlStatement = "select Path, GoldAmount, ExpectedAmount, TrainAmount, TrainLowest, TrainHighest from [dbo].[predict]";

		private readonly string connectionString;

		public PredictResultsBuilder(string connectionString)
		{
			this.connectionString = connectionString;
		}

		public IEnumerable<PredictResult> Build()
		{
			using (var connection = new SqlConnection(this.connectionString))
			using (var command = new SqlCommand(PredictSqlStatement, connection))
			{
				connection.Open();

				var reader = command.ExecuteReader();
				while (reader.Read())
				{
					yield return PredictResult.Factory(reader);
				}
			}
		}
	}
}