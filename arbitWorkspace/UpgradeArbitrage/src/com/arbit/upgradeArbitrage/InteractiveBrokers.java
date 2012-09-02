package com.arbit.upgradeArbitrage;

import com.ib.client.Contract;
import com.ib.client.ContractDetails;
import com.ib.client.EClientSocket;
import com.ib.client.EWrapper;
import com.ib.client.Execution;
import com.ib.client.Order;
import com.ib.client.OrderState;
import com.ib.client.UnderComp;
import com.ib.client.CommissionReport;
import java.util.List;

public class InteractiveBrokers implements EWrapper {

	private EClientSocket m_client = new EClientSocket(this);
	
	private String[] tickTypes = new String[57];
	private int nextValidId = -1;
	
	public InteractiveBrokers(List<String> symbols)
	{
		initializeTickTypes();
		connect();
		
		while(nextValidId==-1)
		{
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		System.out.println("Going to buy " + symbols.size() + " different symbols.");
		for(String symbol:symbols)
		{
			System.out.println("Going to buy 100 shares of " + symbol);
			
			Contract contract = new Contract();
			contract.m_symbol = symbol;
			contract.m_exchange="SMART";
			contract.m_secType="STK";
			contract.m_currency="USD";
			
			Order buyOrder = new Order();
			buyOrder.m_orderType = "MKT";
			buyOrder.m_action = "BUY";
			buyOrder.m_totalQuantity = 100;

			m_client.placeOrder(nextValidId++, contract, buyOrder);
			
			Order sellOrder = new Order();
			sellOrder.m_orderType = "TRAIL";
			sellOrder.m_action = "SELL";
			sellOrder.m_trailingPercent = 1.00;
			sellOrder.m_tif="GTC";
			
			sellOrder.m_totalQuantity = 100;
			
			m_client.placeOrder(nextValidId++, contract, sellOrder);

		}
	}

	private void initializeTickTypes()
	{
		tickTypes[0]="BID_SIZE";
		tickTypes[1]="BID_PRICE";
		tickTypes[2]="ASK_PRICE";
		tickTypes[3]="ASK_SIZE";
		tickTypes[4]="LAST_PRICE";
		tickTypes[5]="LAST_SIZE";
		tickTypes[6]="HIGH";
		tickTypes[7]="LOW";
		tickTypes[8]="VOLUME";
		tickTypes[9]="CLOSE_PRICE";
		tickTypes[10]="BID_OPTION_COMPUTATION";
		tickTypes[11]="ASK_OPTION_COMPUTATION";
		tickTypes[12]="LAST_OPTION_COMPUTATION";
		tickTypes[13]="MODEL_OPTION_COMPUTATION";
		tickTypes[14]="OPEN_TICK";
		tickTypes[15]="LOW_13_WEEK";
		tickTypes[16]="HIGH_13_WEEK";
		tickTypes[17]="LOW_26_WEEK";
		tickTypes[18]="HIGH_26_WEEK";
		tickTypes[19]="LOW_52_WEEK";
		tickTypes[20]="HIGH_52_WEEK";
		tickTypes[21]="AVG_VOLUME";
		tickTypes[22]="OPEN_INTEREST";
		tickTypes[23]="OPTION_HISTORICAL_VOL";
		tickTypes[24]="OPTION_IMPLIED_VOL";
		tickTypes[25]="OPTION_BID_EXCH";
		tickTypes[26]="OPTION_ASK_EXCH";
		tickTypes[27]="OPTION_CALL_OPEN_INTEREST";
		tickTypes[28]="OPTION_PUT_OPEN_INTEREST";
		tickTypes[29]="OPTION_CALL_VOLUME";
		tickTypes[30]="OPTION_PUT_VOLUME";
		tickTypes[31]="INDEX_FUTURE_PREMIUM";
		tickTypes[32]="BID_EXCH";
		tickTypes[33]="ASK_EXCH";
		tickTypes[34]="AUCTION_VOLUME";
		tickTypes[35]="AUCTION_PRICE";
		tickTypes[36]="AUCTION_IMBALANCE";
		tickTypes[37]="MARK_PRICE";
		tickTypes[38]="BID_EFP_COMPUTATION";
		tickTypes[39]="ASK_EFP_COMPUTATION";
		tickTypes[40]="LAST_EFP_COMPUTATION";
		tickTypes[41]="OPEN_EFP_COMPUTATION";
		tickTypes[42]="HIGH_EFP_COMPUTATION";
		tickTypes[43]="LOW_EFP_COMPUTATION";
		tickTypes[44]="CLOSE_EFP_COMPUTATION";
		tickTypes[45]="LAST_TIMESTAMP";
		tickTypes[46]="SHORTABLE";
		tickTypes[47]="FUNDAMENTAL_RATIOS";
		tickTypes[48]="RT_VOLUME";
		tickTypes[49]="HALTED";
		tickTypes[50]="BIDYIELD";
		tickTypes[51]="ASKYIELD";
		tickTypes[52]="LASTYIELD";
		tickTypes[53]="CUST_OPTION_COMPUTATION";
		tickTypes[54]="TRADE_COUNT";
		tickTypes[55]="TRADE_RATE";
		tickTypes[56]="VOLUME_RATE";
	}
	
	private void connect()
	{
		String m_retIpAddress = "";
		int m_retPort = 7496;
		int m_retClientId = 0;
	
		m_client.eConnect(m_retIpAddress, m_retPort, m_retClientId);
		
		if (m_client.isConnected()) {
			System.out.println("Connected to TWS server version " + m_client.serverVersion() + " at " + m_client.TwsConnectionTime());
		}
	}
			
	public void disconnect()
	{
		m_client.eDisconnect();
		System.out.println("Disconnected from TWS server.");
	}

	@Override
	public void error(Exception e) {
		System.out.println("error" + "\te: " + e);
	}

	@Override
	public void error(String str) {
		System.out.println("error" + "\tstr: " + str);
	}

	@Override
	public void error(int id, int errorCode, String errorMsg) {			
		System.out.println("error" + "\tid: " + id + "\terrorCode: " + errorCode + "\terrorMsg: " + errorMsg);
	}

	@Override
	public void connectionClosed() {
		System.out.println("connection closed");
	}

	@Override
	public void tickPrice(int tickerId, int field, double price, int canAutoExecute) {
		System.out.println("tickPrice" + "\ttickerId: " + tickerId + "\tfield: " + field + " " + tickTypes[field] + "\tprice: " + price  + "\tcanAutoExecute: " + canAutoExecute);
	}

	@Override
	public void tickSize(int tickerId, int field, int size) {
		System.out.println("tickSize" + "\ttickerId: " + tickerId + "\tfield: " + field + " " + tickTypes[field] + "\tsize: " + size);
	}

	@Override
	public void tickOptionComputation(int tickerId, int field,
			double impliedVol, double delta, double optPrice,
			double pvDividend, double gamma, double vega, double theta,
			double undPrice) {
		System.out.println("tick option computation");	
	}

	@Override
	public void tickGeneric(int tickerId, int tickType, double value) {
		System.out.println("tickGeneric" + "\ttickerId: " + tickerId + "\ttickType: " + tickType + " " + tickTypes[tickType] + "\tvalue: " + value);
	}

	@Override
	public void tickString(int tickerId, int tickType, String value) {
		System.out.println("tickString" + "\ttickerId: " + tickerId + "\ttickType: "  + tickType + " " + tickTypes[tickType] + "\tvalue: " + value);
	}

	@Override
	public void tickEFP(int tickerId, int tickType, double basisPoints,
			String formattedBasisPoints, double impliedFuture, int holdDays,
			String futureExpiry, double dividendImpact, double dividendsToExpiry) {
		System.out.println("tickEFP");	
	}

	@Override
	public void orderStatus(int orderId, String status, int filled,
			int remaining, double avgFillPrice, int permId, int parentId,
			double lastFillPrice, int clientId, String whyHeld) {
		System.out.println("orderStatus" + "\torderId: " + orderId + "\tstatus: " + status + "\tfilled: " + filled + "\tremaining: " + remaining + "\tavgFillPrice: " + avgFillPrice + "\tpermId: " + permId + "\tparentId:" + parentId + "\tlastFillPrice: "+ lastFillPrice + "\tclientId: " + clientId + "\twhyHeld: " + whyHeld);
	}

	@Override
	public void openOrder(int orderId, Contract contract, Order order,
			OrderState orderState) {
		System.out.println("openOrder" + "\torderId: " + orderId + "\tcontract: " + contract + "\torder: " +order + "\torderState: " + orderState);	
	}

	@Override
	public void openOrderEnd() {
		System.out.println("openOrderEnd");	
	}

	@Override
	public void updateAccountValue(String key, String value, String currency,
			String accountName) {
		System.out.println("updateAccountValue");
	}

	@Override
	public void updatePortfolio(Contract contract, int position,
			double marketPrice, double marketValue, double averageCost,
			double unrealizedPNL, double realizedPNL, String accountName) {
		System.out.println("updatePortfolio");
	}

	@Override
	public void updateAccountTime(String timeStamp) {
		System.out.println("updateAccountTime");	
	}

	@Override
	public void accountDownloadEnd(String accountName) {
		System.out.println("accountDownloadEnd");
	}

	@Override
	public void nextValidId(int orderId) {
		System.out.println("nextValidId" + "\torderId: " + orderId);
		
		//concurrency issues to be fixed here
		nextValidId = orderId;
	}

	@Override
	public void contractDetails(int reqId, ContractDetails contractDetails) {
		System.out.println("contractDetails");
	}

	@Override
	public void bondContractDetails(int reqId, ContractDetails contractDetails) {
		System.out.println("contractDetails");
	}

	@Override
	public void contractDetailsEnd(int reqId) {
		System.out.println("contractDetailsEnd");
	}

	@Override
	public void execDetails(int reqId, Contract contract, Execution execution) {
		System.out.println("execDetails" + "\reqId: " + reqId + "\tcontract: " + contract + "\texecution: " + execution);
	}

	@Override
	public void execDetailsEnd(int reqId) {
		System.out.println("execDetailsEnd");
	}

	@Override
	public void updateMktDepth(int tickerId, int position, int operation,
			int side, double price, int size) {
		System.out.println("updateMktDepth");
	}

	@Override
	public void updateMktDepthL2(int tickerId, int position,
			String marketMaker, int operation, int side, double price, int size) {
		System.out.println("updateMktDepthL2");
	}

	@Override
	public void updateNewsBulletin(int msgId, int msgType, String message,
			String origExchange) {
		System.out.println("updateNewsBulletin");
	}

	@Override
	public void managedAccounts(String accountsList) {
		System.out.println("managedAccounts" +  " accountsList: " + accountsList);
	}

	@Override
	public void receiveFA(int faDataType, String xml) {
		System.out.println("receiveFA");
	}

	@Override
	public void historicalData(int reqId, String date, double open,
			double high, double low, double close, int volume, int count,
			double WAP, boolean hasGaps) {
		System.out.println("historicalData");
	}

	@Override
	public void scannerParameters(String xml) {
		System.out.println("scannerParameters");
	}

	@Override
	public void scannerData(int reqId, int rank,
			ContractDetails contractDetails, String distance, String benchmark,
			String projection, String legsStr) {
		System.out.println("scannerData");
	}

	@Override
	public void scannerDataEnd(int reqId) {
		System.out.println("scannerDataEnd");
	}

	@Override
	public void realtimeBar(int reqId, long time, double open, double high,
			double low, double close, long volume, double wap, int count) {
		System.out.println("realtimeBar");
	}

	@Override
	public void currentTime(long time) {
		System.out.println("currentTime");
	}

	@Override
	public void fundamentalData(int reqId, String data) {
		System.out.println("fundamentalData");
	}

	@Override
	public void deltaNeutralValidation(int reqId, UnderComp underComp) {
		System.out.println("deltaNeutralValidation");	
	}

	@Override
	public void tickSnapshotEnd(int reqId) {
		System.out.println("tickSnapshotEnd" +  "\treqId: " + reqId);
	}

	@Override
	public void marketDataType(int reqId, int marketDataType) {
		System.out.println("marketDataType");
	}

	@Override
	public void commissionReport(CommissionReport commissionReport) {
		System.out.println("commissionReport" + "\tcommissionReport: " + commissionReport);
	}
}