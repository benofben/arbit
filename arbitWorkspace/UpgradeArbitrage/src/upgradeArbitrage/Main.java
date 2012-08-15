package upgradeArbitrage;

import java.io.IOException;

public class Main 
{
	
	// This method is called to start the application
	public static void main (String args[]) 
	{
		InteractiveBrokers interactiveBrokers = new InteractiveBrokers();
		
		// now go fetch symbols from db
		
		// how do we ensure the download of upgrades has already happened?  Time the batches?
		
		/*
		 * Same as before?
		 * Get market data at 9:28AM
		 * Put order in at (bid+ask)/2 with the assumption that is close enough to open price 
		 * If not filled by 9:40AM then cancel
		 * 
		 * Automate exit as well.
		 * 
		 * Close orders at end of day
		 * Check positions at end of day and close those as well. 
		 * 
		 */
		
		try {
			System.out.println("Press ENTER to exit.");
			System.in.read();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		interactiveBrokers.disconnect();
	}
}