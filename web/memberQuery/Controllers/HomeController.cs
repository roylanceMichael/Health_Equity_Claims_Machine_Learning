namespace MemberQuery.Controllers
{
	using System.Configuration;
	using System.Linq;
	using System.Web.Mvc;

	using MemberQuery.Builders;

	public class HomeController : Controller
	{
		public ActionResult Index()
		{
			return this.View();
		}

		public ActionResult PredictResults()
		{
			var connectionString = ConfigurationManager.AppSettings["ConnectionString"];
			return this.View(new PredictResultsBuilder(connectionString).Build().ToList());
		}
	}
}
