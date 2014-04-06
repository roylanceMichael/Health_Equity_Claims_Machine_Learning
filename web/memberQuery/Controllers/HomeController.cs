namespace MemberQuery.Controllers
{
	using System.Collections.Generic;
	using System.Configuration;
	using System.Linq;
	using System.Web.Mvc;

	using MemberQuery.Builders;
	using MemberQuery.Models;

	public class HomeController : Controller
	{
		private readonly string connectionString;

		public HomeController()
		{
			this.connectionString = ConfigurationManager.AppSettings["ConnectionString"];
		}

		public ActionResult Index(string birthYear, string state, string previousCpts)
		{
			if (!string.IsNullOrWhiteSpace(birthYear))
			{
				return this.View(new QueryResultsBuilder(this.connectionString, birthYear, state, previousCpts).Build());
			}

			return this.View(new QueryResults
				                 {
					                 Results = new Dictionary<TransitionRecord, List<EmissionRecord>>()
				                 });
		}

		public ActionResult PredictResults()
		{
			return this.View(new PredictResults(new PredictResultsBuilder(this.connectionString).Build().ToList()));
		}
	}
}
