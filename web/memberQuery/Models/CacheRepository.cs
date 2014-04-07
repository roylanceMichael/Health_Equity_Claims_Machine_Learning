namespace MemberQuery.Models
{
	using System.Data.SqlClient;

	using MemberQuery.Resources;

	using Newtonsoft.Json;

	public class CacheRepository
	{
		private const string BirthYearParam = "@BirthYear";

		private const string LocationParam = "@Location";

		private const string PreviousCptParam = "@PreviousCpt";

		private const string SerializedJsonParam = "@SerializedJson";

		private const string InsertIntoCache =
			"insert into dbo.SerializedResult(BirthYear, Location, PreviousCpt, SerializedJson) values (@BirthYear, @Location, @PreviousCpt, @SerializedJson)";

		private const string SelectFromCache = "select SerializedJson from dbo.SerializedResult where BirthYear = @BirthYear and Location = @Location and PreviousCpt = @PreviousCpt";

		private readonly string connectionString;

		public CacheRepository(string connectionString)
		{
			connectionString.CheckIfArgNull("connectionString");
			this.connectionString = connectionString;
		}

		public QueryResults GetQueryResults(string birthYear, string state, string previousCpts)
		{
			using (var connection = new SqlConnection(this.connectionString))
			using (var command = new SqlCommand(SelectFromCache, connection))
			{
				connection.Open();

				command.Parameters.AddWithValue(BirthYearParam, birthYear);
				command.Parameters.AddWithValue(LocationParam, state);
				command.Parameters.AddWithValue(PreviousCptParam, previousCpts);

				var json = command.ExecuteScalar();

				if (json != null)
				{
					return JsonConvert.DeserializeObject<QueryResults>(json.ToString());
				}
			}

			return null;
		}

		public void CacheQueryResults(string birthYear, string state, string previousCpts, QueryResults queryResults)
		{
			using (var connection = new SqlConnection(this.connectionString))
			using (var command = new SqlCommand(InsertIntoCache, connection))
			{
				connection.Open();

				command.Parameters.AddWithValue(BirthYearParam, birthYear);
				command.Parameters.AddWithValue(LocationParam, state);
				command.Parameters.AddWithValue(PreviousCptParam, previousCpts);
				command.Parameters.AddWithValue(SerializedJsonParam, JsonConvert.SerializeObject(queryResults));

				command.ExecuteNonQuery();
			}
		}
	}
}