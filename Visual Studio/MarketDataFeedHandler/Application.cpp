#include "Application.h"

void Application::onCreate( const FIX::SessionID& sessionID ) 
{
	std::cout << "Created: " << sessionID << std::endl;
}

void Application::onLogon( const FIX::SessionID& sessionID )
{
	std::cout << "Logon: " << sessionID << std::endl;
	subscribe(sessionID);
	//getSecurities(sessionID);
}

void Application::onLogout( const FIX::SessionID& sessionID )
{
	std::cout << "Logout: " << sessionID << std::endl;
}

void Application::toAdmin( FIX::Message& message, const FIX::SessionID& sessionID) 
{
	// if logon message, add password
	if (message.getHeader().getField(FIX::FIELD::MsgType)=="A")
	{
		char* password="12345678";
		message.getHeader().setField(FIX::FIELD::RawData, password);
	}

	std::cout << "toAdmin: " << message << std::endl;
}

void Application::toApp( FIX::Message& message, const FIX::SessionID& sessionID )throw( FIX::DoNotSend )
{
	std::cout << "toApp: " << message << std::endl;
}

void Application::fromAdmin( const FIX::Message& message, const FIX::SessionID& sessionID) throw( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::RejectLogon ) 
{
	std::cout << "fromAdmin: " << message << std::endl;	
}

void Application::fromApp( const FIX::Message& message, const FIX::SessionID& sessionID ) throw( FIX::FieldNotFound, FIX::IncorrectDataFormat, FIX::IncorrectTagValue, FIX::UnsupportedMessageType )
{
	crack( message, sessionID );
	//std::cout << "fromApp: " << message << std::endl;
}

void Application::onMessage( const FIX42::MarketDataSnapshotFullRefresh& message, const FIX::SessionID& )
{
	//cout << "onMessage: " << message.toString() << endl;
	
	FIX::Symbol symbol;
	message.getField(symbol);
	
	for(int i=1;i<message.groupCount(FIX::FIELD::NoMDEntries);i++)
	{
		FIX42::MarketDataSnapshotFullRefresh::NoMDEntries noMDEntries;
		message.getGroup(i, noMDEntries);

		FIX::MDEntryType mDEntryType;
		noMDEntries.getField(mDEntryType);

		FIX::MDEntryPx mDEntryPx;
		noMDEntries.getField(mDEntryPx);

		FIX::MDEntrySize mDEntrySize;
		noMDEntries.getField(mDEntrySize);

		cout << symbol << " " << mDEntryType << " " << mDEntryPx << " " << mDEntrySize << endl;
	}
	cout << endl;
}

void Application::onMessage( const FIX42::SecurityDefinition& message, const FIX::SessionID& )
{
	//cout << "Got a symbol " << message.getField(FIX::FIELD::SecurityID) << endl;
	//cout << message.toString() << endl;
	
	ofstream ofile( "symbols.txt", ios::app );
	
	if(message.isSetField(FIX::FIELD::SecurityExchange))
		ofile << message.getField(FIX::FIELD::SecurityExchange);
	ofile << ",";

	if(message.isSetField(FIX::FIELD::SecurityType))
		ofile << message.getField(FIX::FIELD::SecurityType);
	ofile << ",";

	if(message.isSetField(FIX::FIELD::Symbol))
		ofile << message.getField(FIX::FIELD::Symbol);
	ofile << ",";

	if(message.isSetField(FIX::FIELD::MaturityMonthYear))
		ofile << message.getField(FIX::FIELD::MaturityMonthYear);
	ofile << ",";

	if(message.isSetField(FIX::FIELD::SecurityID))
		ofile << message.getField(FIX::FIELD::SecurityID);
	ofile << endl;
	
	ofile.close();
}

void Application::getSecurities( const FIX::SessionID& sessionID )
{
	char buffer[33];

	try
	{
		FIX42::SecurityDefinitionRequest message(
			FIX::SecurityReqID(itoa(time(NULL), buffer, 10)),
			FIX::SecurityRequestType(0));

		message.setField(FIX::SecurityType("FUT"));
		FIX::Session::sendToTarget(message, sessionID);
	}
	catch(FIX::SessionNotFound e)
	{
		std::cout << e.what() << std::endl;
	}
}

void Application::subscribe( const FIX::SessionID& sessionID )
{
	char buffer[33];

	// let's create some subscriptions...
	if(sessionID.getTargetCompID()=="TTDEV9P")
	{
		try
		{
			FIX42::MarketDataRequest message( 
				FIX::MDReqID( itoa(time(NULL), buffer, 10) ),
				FIX::SubscriptionRequestType( FIX::SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES ),
				FIX::MarketDepth( 0 )); //Full Book

			message.setField(FIX::MDUpdateType( 0 )); //Full Refresh
			message.setField(FIX::AggregatedBook(true));

			FIX42::MarketDataRequest::NoMDEntryTypes marketDataEntryGroupBid;
			marketDataEntryGroupBid.set(FIX::MDEntryType(FIX::MDEntryType_BID));
			message.addGroup( marketDataEntryGroupBid );

			FIX42::MarketDataRequest::NoMDEntryTypes marketDataEntryGroupOffer;
			marketDataEntryGroupOffer.set(FIX::MDEntryType(FIX::MDEntryType_OFFER));
			message.addGroup( marketDataEntryGroupOffer );

			//message.addGroup(addFDAX());
			message.addGroup(addOil());
			//message.addGroup(addZN());

			FIX::Session::sendToTarget(message, sessionID);
		}
		catch(FIX::SessionNotFound e)
		{
			std::cout << e.what() << std::endl;
		}
	}
}

FIX42::MarketDataRequest::NoRelatedSym Application::addFDAX()
{
	FIX42::MarketDataRequest::NoRelatedSym symbolGroup;
	symbolGroup.set(FIX::Symbol("DAX"));
	symbolGroup.set(FIX::SecurityID("XETRDE0008469008"));
	symbolGroup.set(FIX::SecurityExchange("Eurex"));

	return symbolGroup;
}

FIX42::MarketDataRequest::NoRelatedSym Application::addOil()
{
	// CME-A,FUT,CL,201001,00A0AK00CLZ
	FIX42::MarketDataRequest::NoRelatedSym symbolGroup;
	symbolGroup.set(FIX::SecurityExchange("CME-A"));
	symbolGroup.set(FIX::SecurityType("FUT"));
	symbolGroup.set(FIX::Symbol("CL"));
	symbolGroup.set(FIX::MaturityMonthYear("201001"));
	symbolGroup.set(FIX::SecurityID("00A0AK00CLZ"));	

	return symbolGroup;
}

FIX42::MarketDataRequest::NoRelatedSym Application::addZN()
{
	FIX42::MarketDataRequest::NoRelatedSym symbolGroup;
	symbolGroup.set(FIX::SecurityID("00A0CK00ZNZ"));
	symbolGroup.set(FIX::Symbol("ZN"));
	symbolGroup.set(FIX::MaturityMonthYear("201003"));
	symbolGroup.set(FIX::SecurityExchange("CBOT"));

	return symbolGroup;
}