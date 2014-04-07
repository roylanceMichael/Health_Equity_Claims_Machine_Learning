namespace MemberQuery.Models
{
	using System;
	using System.Collections.Generic;
	using System.Linq;

	public class PredictResults
	{
		private IEnumerable<PredictResult> predictResults;
 
		public PredictResults(IEnumerable<PredictResult> predictResults)
		{
			if (predictResults == null)
			{
				return;
			}

			this.predictResults = predictResults.ToList();

			this.GoldToExpectedAverageVariation =
				Math.Round(
					this.predictResults.Where(result => result.ExpectedAmount.HasValue && result.GoldAmount.HasValue)
						.Average(result => result.GoldExpectedVariation.Value),
					2);

			// calculate variance
			foreach (var prediction in this.predictResults.Where(prediction => prediction.GoldExpectedVariation.HasValue))
			{
				prediction.GoldExpectedStandardDeviation = Math.Round(Math.Pow(prediction.GoldExpectedVariation.Value - this.GoldToExpectedAverageVariation, 2), 2);
			}

			this.GoldToExpectedStandardDeviation = Math.Round(Math.Sqrt(this.predictResults.Average(result => result.GoldExpectedStandardDeviation)), 2);
		}

		public IEnumerable<PredictResult> Predictions
		{
			get
			{
				return this.predictResults;
			}

			set
			{
				this.predictResults = value;
			}
		}

		public double GoldToExpectedAverageVariation { get; private set; }

		public double GoldToExpectedStandardDeviation { get; private set; }

	}
}