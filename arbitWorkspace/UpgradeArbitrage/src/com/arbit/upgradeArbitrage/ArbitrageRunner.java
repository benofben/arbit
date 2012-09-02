package com.arbit.upgradeArbitrage;

import java.sql.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import oracle.jdbc.pool.OracleDataSource;

public class ArbitrageRunner 
{
	Timer timer = new Timer();
	
	public static void main (String args[]) 
	{
		new ArbitrageRunner();
	}
	
	public ArbitrageRunner()
	{
		Calendar nextTradeCalendar = getNextTradeCalendar();
		System.out.println("The next time I'm going to trade is " + nextTradeCalendar.getTime().toString() + "."); 
        timer.schedule(new UpgradeArbitrageTask(), nextTradeCalendar.getTime());
        //timer.schedule(new UpgradeArbitrageTask(), 2000);
	}
	
	class UpgradeArbitrageTask extends TimerTask 
	{
		public void run()
		{
			Calendar now = Calendar.getInstance();
			System.out.println("Running upgrade arbitrage at " + now.getTime().toString() + ".");
			
			Calendar queryCalendar = (Calendar) now.clone();
			queryCalendar.add(Calendar.DATE, -1);
			List<String> symbols = getUpgradedSymbols(queryCalendar);	
			
			InteractiveBrokers interactiveBrokers = new InteractiveBrokers(symbols);	
			try {
				Thread.sleep(60 * 1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			interactiveBrokers.disconnect();

			Calendar nextTradeCalendar = getNextTradeCalendar();
			System.out.println("The next time I'm going to trade is " + nextTradeCalendar.getTime().toString() + ".");
			timer.schedule(new UpgradeArbitrageTask(), nextTradeCalendar.getTime());
		}
	}
	
	private static Calendar getNextTradeCalendar(){
		Calendar calendar930AM = Calendar.getInstance();
		calendar930AM.set(Calendar.HOUR_OF_DAY, 9);
		calendar930AM.set(Calendar.MINUTE, 30);
		calendar930AM.set(Calendar.SECOND, 00);
		
		Calendar nextTradeCalendar = Calendar.getInstance();
		
		// if it's after 9:30am or a weekend
		if(nextTradeCalendar.after(calendar930AM) || isWeekend(nextTradeCalendar))
		{	
			// advance the date to tomorrow
			nextTradeCalendar.add(Calendar.DATE, 1);
			
			// advance further if we're in the weekend
			while(isWeekend(nextTradeCalendar))
				nextTradeCalendar.add(Calendar.DATE, 1);
		}
		
		nextTradeCalendar.set(Calendar.HOUR_OF_DAY, 9);
		nextTradeCalendar.set(Calendar.MINUTE, 30);
		nextTradeCalendar.set(Calendar.SECOND, 00);
		return nextTradeCalendar;
	}
	
	private static boolean isWeekend(Calendar calendar)
	{
		// might consider extending to isTradingDay which would include a proper calendar of when the markets are open.
		if(calendar.get(Calendar.DAY_OF_WEEK)==Calendar.SATURDAY || calendar.get(Calendar.DAY_OF_WEEK)==Calendar.SUNDAY)
				return true;
		return false;
	}
	
	private static List<String> getUpgradedSymbols(Calendar calendar) {
		//Format should be like '22-Aug-12'
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("dd-MMM-yy");
		String dateString = simpleDateFormat.format(calendar.getTime());
		System.out.println("Going to use analyst upgrades from " + dateString + ".");
		dateString = "'" + simpleDateFormat.format(calendar.getTime()) + "'";
		
		List<String> symbols = new ArrayList<String>();
		
		try {
			OracleDataSource oracleDataSource = new OracleDataSource();
			oracleDataSource.setURL("jdbc:oracle:thin:arbit/arbit@localhost:1521:orcl");
			Connection connection;
			connection = oracleDataSource.getConnection();

			Statement statement = connection.createStatement();
			
			String queryString = "SELECT TICKER FROM RATINGSCHANGES WHERE RATINGSCHANGETYPE='Upgrade' AND RATINGSCHANGEDATE=" + dateString;
			ResultSet resultSet = statement.executeQuery (queryString);

			while (resultSet.next())
				symbols.add(resultSet.getString(1));
			
			resultSet.close();
			statement.close();
			connection.close();

		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		return symbols;
	}
}