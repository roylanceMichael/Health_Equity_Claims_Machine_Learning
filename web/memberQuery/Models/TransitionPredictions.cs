namespace MemberQuery.Models
{
	using System.Collections.Generic;
	using System.Linq;

	using MemberQuery.Resources;

	public class TransitionPredictions
	{
		private readonly IEnumerable<TransitionEmissions> transitionEmissions;

		private readonly double minimumSuggestedAmount;

		public TransitionPredictions(IEnumerable<TransitionEmissions> transitionEmissions)
		{
			transitionEmissions.CheckIfArgNull("transitionEmissions");

			this.transitionEmissions = transitionEmissions.OrderByDescending(emissions => emissions.Probability);

			if (!this.transitionEmissions.Any())
			{
				return;
			}

			var expectedAmounts = new List<double>();
			var standardDeviations = new List<double>();

			var runningProbability = (double)0;
			var i = 0;
			while (runningProbability < 0.5)
			{
				var transitionEmission = this.transitionEmissions.ElementAt(i);
				expectedAmounts.Add(transitionEmission.ExpectedValue);
				standardDeviations.Add(transitionEmission.StandardDeviation);
				runningProbability += transitionEmission.Probability;
				i++;
			}

			this.minimumSuggestedAmount = expectedAmounts.Average() + standardDeviations.Average();
		}

		public IEnumerable<TransitionEmissions> TransitionEmissions
		{
			get
			{
				return this.transitionEmissions;
			}
		}

		public double MinimumSuggestedAmount
		{
			get
			{
				return this.minimumSuggestedAmount;
			}
		}
	}
}