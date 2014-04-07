namespace MemberQuery.Builders
{
	using System;
	using System.Collections.Generic;
	using System.Data.SqlClient;
	using System.Linq;

	using MemberQuery.Models;
	using MemberQuery.Resources;

	public class QueryResultsBuilder : IBuilder<QueryResults>
	{
		private const string CptCodeParam = "@CptCode";

		private const string FromCptCodeParam = "@FromCptCode";

		private const string EmissionCptCodeParam = "@CptCodeParam";

		private const string CptToCcsSql = "select [ CcsCode] from [dbo].[CptToCssDict] where CptCode = " + CptCodeParam;

		private const string TransitionRecordSql = "select From_CPT, To_CPT, Probability from [dbo].[ageLocationtrainTransitions] where From_CPT = " + FromCptCodeParam;

		private const string EmissionRecordSql = "select CPT, Total_Amount, Probability from [dbo].[ageLocationEmissions] where CPT = " + EmissionCptCodeParam;

		private readonly string connectionString;

		private readonly string birthYear;

		private readonly string state;

		private readonly string previousCpts;

		public QueryResultsBuilder(string connectionString, string birthYear, string state, string previousCpts)
		{
			connectionString.CheckIfArgNull("connectionString");
			birthYear.CheckIfArgNull("birthYear");
			state.CheckIfArgNull("state");
			previousCpts.CheckIfArgNull("previousCpts");

			this.connectionString = connectionString;
			this.birthYear = birthYear.Trim();
			this.state = state.Trim();
			this.previousCpts = previousCpts.Trim();
		}

		public QueryResults Build()
		{
			// get ccs code
			var ccsCodes = new List<string>();

			using (var connection = new SqlConnection(this.connectionString))
			{
				connection.Open();

				foreach (var cptCode in this.GetPreviousCpts())
				{
					using (var command = new SqlCommand(CptToCcsSql, connection))
					{
						command.Parameters.AddWithValue(CptCodeParam, cptCode);
						var result = command.ExecuteScalar();

						if (result != null)
						{
							ccsCodes.Add(result.ToString());
						}
					}
				}
				
				// just do last one for now...
				var lastCcsCode = ccsCodes.LastOrDefault();
				if (lastCcsCode == null)
				{
					return new QueryResults();
				}

				var fromTransition = this.GetAge() + "_" + this.state + lastCcsCode;

				var transitionRecords = new HashSet<TransitionRecord>();
				using (var command = new SqlCommand(TransitionRecordSql, connection))
				{
					command.Parameters.AddWithValue(FromCptCodeParam, fromTransition);

					var reader = command.ExecuteReader();

					while (reader.Read())
					{
						transitionRecords.Add(TransitionRecord.Factory(reader));
					}

					reader.Close();
				}

				var transitionEmissions = new HashSet<TransitionEmissions>();

				foreach (var transitionRecord in transitionRecords)
				{
					var emissionKey = transitionRecord.FromTransition + "_" + transitionRecord.ToTransition;
					using (var command = new SqlCommand(EmissionRecordSql, connection))
					{
						command.Parameters.AddWithValue(EmissionCptCodeParam, emissionKey);

						var reader = command.ExecuteReader();
						var emissions = new List<EmissionRecord>();
						while (reader.Read())
						{
							emissions.Add(EmissionRecord.Factory(reader));
						}

						var transitionEmission = new TransitionEmissions(transitionRecord, emissions);
						transitionEmissions.Add(transitionEmission);
						reader.Close();
					}
				}

				return new QueryResults { Results = new TransitionPredictions(transitionEmissions) };
			}
		}

		private IEnumerable<string> GetPreviousCpts()
		{
			return this.previousCpts.Split(',');
		}

		private string GetAge()
		{
			int actualBirthYear;

			var currentYear = DateTime.Now.Year;
			
			if (!int.TryParse(this.birthYear, out actualBirthYear))
			{
				return "UnknownAge";
			}
			
			if (actualBirthYear - currentYear < 30)
			{
				return "Under30";
			}

			return actualBirthYear - currentYear < 60 ? "Under60" : "Over60";
		}
	}
}