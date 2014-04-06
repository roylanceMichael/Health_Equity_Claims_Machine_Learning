namespace MemberQuery.Models
{
	using System.Collections.Generic;

	public class QueryResults
	{
		public Dictionary<TransitionRecord, List<EmissionRecord>> Results { get; set; }
	}
}