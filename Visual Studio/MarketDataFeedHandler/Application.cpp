#include "Application.h"

void Application::onCreate( const FIX::SessionID& sessionID ) 
{
	std::cout << "Created: " << sessionID << std::endl;
}

void Application::onLogon( const FIX::SessionID& sessionID )
{
	std::cout << "Logon: " << sessionID << std::endl;
	subscribeOil( sessionID );
	//subscribeFDAX( sessionID );
	getSecurities( sessionID );
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
	std::cout << "fromApp: " << message << std::endl;
}

void Application::onMessage( const FIX42::MarketDataSnapshotFullRefresh& message, const FIX::SessionID& )
{
	cout << "onMessage: " << message.toString() << endl;
	
	FIX::Symbol symbol;
	message.get(symbol);

	FIX42::MarketDataSnapshotFullRefresh::NoMDEntries noMDEntries;
	message.getGroup(1, noMDEntries);

	FIX::MDEntryType mDEntryType;
	noMDEntries.getField(mDEntryType);

	//cout << mDEntryType << endl;
}

void Application::onMessage( const FIX42::SecurityDefinition& message, const FIX::SessionID& )
{
	//cout << "Got a symbol " << message.getField(FIX::FIELD::SecurityID) << endl;
	//cout << message.toString() << endl;

	ofstream ofile( "symbols.txt", ios::app );
	ofile 
		<< message.getField(FIX::FIELD::SecurityExchange) << "," 
		<< message.getField(FIX::FIELD::SecurityType) << ","
		<< message.getField(FIX::FIELD::Symbol) << "," 
		<< message.getField(FIX::FIELD::MaturityMonthYear) << "," 
		<< message.getField(FIX::FIELD::SecurityID)		
		<< endl;
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

		FIX::Session::sendToTarget(message, sessionID);
	}
	catch(FIX::SessionNotFound e)
	{
		std::cout << e.what() << std::endl;
	}
}

void Application::subscribeFDAX( const FIX::SessionID& sessionID )
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
				FIX::MarketDepth( 0 ));

			message.setField(FIX::MDUpdateType( 0 ));
			message.setField(FIX::AggregatedBook(true));

			FIX42::MarketDataRequest::NoMDEntryTypes marketDataEntryGroup;
			marketDataEntryGroup.set(FIX::MDEntryType(FIX::MDEntryType_BID));
			marketDataEntryGroup.set(FIX::MDEntryType(FIX::MDEntryType_OFFER));
			message.addGroup( marketDataEntryGroup );

			FIX42::MarketDataRequest::NoRelatedSym symbolGroup;
			symbolGroup.set(FIX::Symbol("DAX"));
			symbolGroup.set(FIX::SecurityID("XETRDE0008469008"));
			symbolGroup.set(FIX::SecurityExchange("Eurex"));

			message.addGroup( symbolGroup );						

			FIX::Session::sendToTarget(message, sessionID);
		}
		catch(FIX::SessionNotFound e)
		{
			std::cout << e.what() << std::endl;
		}
	}
}

void Application::subscribeOil( const FIX::SessionID& sessionID )
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
				FIX::MarketDepth( 0 ));

			message.setField(FIX::MDUpdateType( 0 ));
			message.setField(FIX::AggregatedBook(true));

			FIX42::MarketDataRequest::NoMDEntryTypes marketDataEntryGroup;
			marketDataEntryGroup.set(FIX::MDEntryType(FIX::MDEntryType_BID));
			marketDataEntryGroup.set(FIX::MDEntryType(FIX::MDEntryType_OFFER));
			message.addGroup( marketDataEntryGroup );

			FIX42::MarketDataRequest::NoRelatedSym symbolGroup;
			symbolGroup.set(FIX::Symbol("CL"));
			symbolGroup.set(FIX::MaturityMonthYear("201001"));
			symbolGroup.set(FIX::SecurityExchange("CME-A"));
			//symbolGroup.set(FIX::SecurityID("00A0CK006BZ"));	

			message.addGroup( symbolGroup );						

			FIX::Session::sendToTarget(message, sessionID);
		}
		catch(FIX::SessionNotFound e)
		{
			std::cout << e.what() << std::endl;
		}
	}
}
