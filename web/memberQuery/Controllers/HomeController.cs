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
				var cacheRepository = new CacheRepository(this.connectionString);
				var results = cacheRepository.GetQueryResults(birthYear, state, previousCpts);

				if (results != null)
				{
					return this.View(results);
				}

				var queryResults = new QueryResultsBuilder(this.connectionString, birthYear, state, previousCpts).Build();
				cacheRepository.CacheQueryResults(birthYear, state, previousCpts, queryResults);
				return this.View(queryResults);
			}

			return this.View(new QueryResults
				                 {
					                 Results = new TransitionPredictions(new List<TransitionEmissions>())
				                 });
		}

		public ActionResult PredictResults()
		{
			return this.View(new PredictResults(new PredictResultsBuilder(this.connectionString).Build().ToList()));
		}

		public ActionResult NewMemberPredictions()
		{
			return this.View(new NewMemberPredictionsBuilder(this.connectionString).Build());
		}
	}
}
