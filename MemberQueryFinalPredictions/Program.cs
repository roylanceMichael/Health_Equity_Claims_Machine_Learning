namespace MemberQueryFinalPredictions
{
	using System;
	using System.Collections.Generic;
	using System.Configuration;
	using System.Data;
	using System.Data.SqlClient;
	using System.Globalization;

	using MemberQuery.Builders;

	public class Program
	{
		private const string ConnectionString = "ConnectionString";

		private const string NewMemberIdParam = "@NewMemberID";

		private const string DependentIdParam = "@DependentID";

		private const string RecommendedBalanceParam = "@RecommendedBalance";

		private const string SufficientAmountParam = "@SufficientAmount";

		private const string NewMemberBalancePredictionsSql = "select NewMemberID, DependentID, BirthYear, State, LastCPTCode, CachedBalance from dbo.NewMemberBalancePredictions";

		private const string UpdateNewMemberBalancePredictionSql = "update dbo.NewMemberBalancePredictions set SufficientAmount = @SufficientAmount, RecommendedBalance = @RecommendedBalance where NewMemberID = @NewMemberID and DependentID = @DependentID";

		public static void Main(string[] args)
		{
			var connectionString = ConfigurationManager.AppSettings[ConnectionString];

			var balanceTuples = new List<BalanceTuple>();

			Console.WriteLine("Starting Calculations...");

			using (var sqlConnection = new SqlConnection(connectionString))
			{
				using (var sqlCommand = new SqlCommand(NewMemberBalancePredictionsSql, sqlConnection))
				{
					sqlConnection.Open();

					var reader = sqlCommand.ExecuteReader();

					while (reader.Read())
					{
						balanceTuples.Add(BalanceTuple.Factory(reader));
					}

					reader.Close();
				}

				Console.WriteLine("Found " + balanceTuples.Count);
				var iteration = 1;
				foreach (var balanceTuple in balanceTuples)
				{
					Console.WriteLine("Processing " + iteration + " / " + balanceTuples.Count);
					iteration++;

					var queryResults = new QueryResultsBuilder(
						connectionString,
						balanceTuple.BirthYear.ToString(CultureInfo.CurrentCulture),
						balanceTuple.State,
						balanceTuple.LastCptCode).Build();

					balanceTuple.RecommendedBalance = queryResults.Results.MinimumSuggestedAmount;
					double actualBalance;
					double.TryParse(balanceTuple.CachedBalance, out actualBalance);

					balanceTuple.SufficientAmount = actualBalance > balanceTuple.RecommendedBalance ? 1 : 0;

					using (var command = new SqlCommand(UpdateNewMemberBalancePredictionSql, sqlConnection))
					{
						command.Parameters.AddWithValue(NewMemberIdParam, balanceTuple.NewMemberId);
						command.Parameters.AddWithValue(DependentIdParam, balanceTuple.DependentId);
						command.Parameters.AddWithValue(RecommendedBalanceParam, balanceTuple.RecommendedBalance);
						command.Parameters.AddWithValue(SufficientAmountParam, balanceTuple.SufficientAmount);
						command.ExecuteNonQuery();
					}
				}
			}
		}

		private class BalanceTuple
		{
			public int NewMemberId { get; private set; }

			public int DependentId { get; private set; }

			public int BirthYear { get; private set; }

			public string State { get; private set; }

			public string LastCptCode { get; private set; }

			public string CachedBalance { get; private set; }

			public double RecommendedBalance { get; set; }

			public int SufficientAmount { get; set; }

			public static BalanceTuple Factory(IDataRecord dataReader)
			{
				return new BalanceTuple
					       {
						       NewMemberId = dataReader.GetInt32(0),
									 DependentId = dataReader.GetInt32(1),
									 BirthYear = dataReader.GetInt32(2),
									 State = dataReader.GetString(3),
									 LastCptCode = dataReader.GetString(4),
									 CachedBalance = dataReader.GetString(5)
					       };
			}
		}
	}
}
