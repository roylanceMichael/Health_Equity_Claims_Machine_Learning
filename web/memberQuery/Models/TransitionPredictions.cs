namespace MemberQuery.Models
{
	using System.Collections.Generic;
	using System.Linq;

	public class TransitionPredictions
	{
		public TransitionPredictions(IEnumerable<TransitionEmissions> transitionEmissions)
		{
			if (transitionEmissions == null)
			{
				return;
			}

			this.TransitionEmissions = transitionEmissions.OrderByDescending(emissions => emissions.Probability);

			if (!this.TransitionEmissions.Any())
			{
				return;
			}

			var expectedAmounts = new List<double>();
			var standardDeviations = new List<double>();

			var runningProbability = (double)0;
			var i = 0;
			while (runningProbability < 0.5)
			{
				var transitionEmission = this.TransitionEmissions.ElementAt(i);
				expectedAmounts.Add(transitionEmission.ExpectedValue);
				standardDeviations.Add(transitionEmission.StandardDeviation);
				runningProbability += transitionEmission.Probability;
				i++;
			}

			this.MinimumSuggestedAmount = expectedAmounts.Average() + standardDeviations.Average();
		}

		public IEnumerable<TransitionEmissions> TransitionEmissions { get; set; }

		public double MinimumSuggestedAmount { get; set; }
	}
}