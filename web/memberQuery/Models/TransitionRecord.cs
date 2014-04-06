namespace MemberQuery.Models
{
	using System.Data.SqlClient;

	public class TransitionRecord
	{
		public string FromTransition { get; set; }

		public string ToTransition { get; set; }

		public double Probability { get; set; }

		public static TransitionRecord Factory(SqlDataReader reader)
		{
			double doubleValue;

			if (!double.TryParse(reader.GetString(2), out doubleValue))
			{
				doubleValue = 0;
			}

			return new TransitionRecord
				       {
					       FromTransition = reader.GetString(0),
								 ToTransition = reader.GetString(1),
								 Probability = doubleValue
				       };
		}
	}
}